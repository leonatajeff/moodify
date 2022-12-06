import time
from flask import Flask, request, json, session, redirect, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import openai
import databaseManager

app = Flask(__name__, static_folder="../build", static_url_path='/')

CLIENT_ID="aaf84179409a48649643d1dca7021d77"
CLIENT_SECRET="c1432d11a176489194f6eb767172be9e"
openai.api_key = "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"
REDIRECT_URI="https://8080-cs-184908628077-default.cs-us-east1-vpcf.cloudshell.dev/"
PERMISSIONS="user-library-read user-read-recently-played user-read-playback-state"
app.config.update(SECRET_KEY=CLIENT_SECRET)



@app.route('/')
def index():
    return app.send_static_file('index.html')
    
@app.route('/api/authorize')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return jsonify({
        'auth_endpoint': auth_url
    })

@app.route('/api/registerToken', methods=['POST'])
def register_token():
    data = json.loads(request.data) 
    sp_oauth = create_spotify_oauth()
    token_info = sp_oauth.get_access_token(data['code'])
    session['token_info'] = token_info
    return token_info

@app.route('/api/uploadTest')
def uploadImages():
    # this code will probably end up being injected into our image generation chunk, but i'll just throw it here for now

    # uploads an image from a url - which is how we retrieve the generated image from the API

    # dummy data for demonstration purposes - we will get this data from the spotify api
    username = "testuser1"
    favGenre = 'rock'
    prompt = 'beach house space song'
    imageUrl = 'https://cdn.discordapp.com/attachments/1024113488483864669/1033931366573805568/unknown.png'
    
        
    # NOTE: upload code will be moved to the image generation route of the api

    databaseManager.upload(username, favGenre, prompt, imageUrl)

@app.route('/api/images')
def fetchImages():
    # Retrieving data
    return databaseManager.getImages()  

@app.route('/api/userImages')
def fetchUserImages():
    # Retrieving data for past moods page
    username = 'testuser'
    # retrieve username from spotify api and send it in 
    try:
        token_info = check_token()
    except:
        print('user not logged in')
        return redirect('/')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.me()
    username = results['username'] # not sure if this is the right attribute I have to see what this returns
    return databaseManager.getUserImages(username)

@app.route('/api/getPrompt', methods=['GET'])
def get_prompt():
    '''
        GET: Generated prompt from user's top listening history

        Using
         - time_range: 4 weeks of listening data to determine top tracks
         - limit: How many songs to return

        Helpful References for Future Enhancement:
        https://developer.spotify.com/console/get-audio-analysis-track/
        https://towardsdatascience.com/reverse-engineering-spotify-wrapped-ai-using-python-452b58ad1a62
    '''
    try:
        token_info = check_token()
    except:
        print('user not logged in')
        return redirect('/')

    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = sp.current_user_recently_played(5)  #top tracks is broken TO-DO

    song_names = []

    for item in top_tracks['items']:
        track = item['track']
        full_string = f"{track['name']} by {track['artists'][0]['name']}"
        print(full_string)
        song_names.append(full_string)
   
    # TO-DO: Does the artist name cause more harm or good to prompt generation?
    prompt = gen_prompt_helper(song_names) #returns a string 

    return prompt

@app.route('/api/getImage', methods=['GET'])
def get_image():
    # Api: Image Generation
    # https://beta.openai.com/docs/guides/images/introduction
    prompt = get_prompt()
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )

    image_url = response['data'][0]['url']
    print(image_url)

    ## I'm pretty sure this is where we will want to upload the user information since we have the prompt and the image url here
    ## upload data with database manager - databaseManager.upload(username, favGenre, prompt, imageUrl)
    return image_url
   
def check_token():
    token_info = session.get('token_info', None)
    if not token_info:
        raise Exception("Token error")
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

# Universal Functions
def create_spotify_oauth():
  return SpotifyOAuth(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=PERMISSIONS,
    cache_path='.spotipyoauthcache'
    )

# Helper Function for Prompt Generation
def gen_prompt_helper(list_of_songs):
    '''
        Helper Function that uses openai Completion to generate a prompt. 
        Takes in a list containing the users top songs.
    '''
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"\nHuman: Create a creative prompt for DALL-E image generation that describes my mood over these songs but dont list the songs in the prompt and instead replace the song names with a creative visual description about the song title: {list_of_songs[0]}, {list_of_songs[1]}, {list_of_songs[2]}, {list_of_songs[3]}, {list_of_songs[4]}",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
        )
    
    text = response["choices"][0]["text"]
    
    return text

