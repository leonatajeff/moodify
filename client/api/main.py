import time
from flask import Flask, request, json, session, redirect, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import openai
import databaseManager

app = Flask(__name__, static_folder="../build", static_url_path='/')

CLIENT_ID=""
CLIENT_SECRET=""
openai.api_key = ""
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

@app.route('/api/getPrompt', methods=['GET'])
def get_prompt():
    '''
        GET: Generated prompt from user's listening history

        Using
         - seed_artists - a list of artist IDs, URIs or URLs
         - seed_tracks - a list of track IDs, URIs or URLs

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
    results = sp.current_user_recently_played(2)

    song_names = []

    for item in results['items']:
        track = item['track']
        song_names.append(track['name'])

    prompt = "An impressionist painting of " + song_names[0] + " " + song_names[1]

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

'''
def get_audio_feature(top_track_id):
    # Returns the audio feature data for the users top track
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    audio_info = sp.audio_features(tracks=[])
    
    return audio_info

def parse_audio_features()
    # Clean up and give meaning to certain features.

def image_gen_string(audio_info, song_title, artist_name):
    song_title example -> Space Song
    artist_name example -> Beach House
    Example of the data we are working with here from audio_info
        {
            "audio_features": [
                {
                "acousticness": 0.00242,
                "analysis_url": "https://api.spotify.com/v1/audio-analysis/2takcwOaAZWiXQijPHIx7B\n",
                "danceability": 0.585, 
                "duration_ms": 237040,
                "energy": 0.842,
                "id": "2takcwOaAZWiXQijPHIx7B",
                "instrumentalness": 0.00686,
                "key": 9,
                "liveness": 0.0866,
                "loudness": -5.883,
                "mode": 0,
                "speechiness": 0.0556,
                "tempo": 118.211,
                "time_signature": 4,
                "track_href": "https://api.spotify.com/v1/tracks/2takcwOaAZWiXQijPHIx7B\n",
                "type": "audio_features",
                "uri": "spotify:track:2takcwOaAZWiXQijPHIx7B",
                "valence": 0.428
                }
            ]
        }
'''


