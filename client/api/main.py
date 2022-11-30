import time
from flask import Flask, request, json, session, redirect, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google.cloud import datastore
from google.cloud import storage
from werkzeug.datastructures import FileStorage 
from PIL import Image
from io import BytesIO
import requests
import openai

app = Flask(__name__, static_folder="../build", static_url_path='/')

CLIENT_ID=""
CLIENT_SECRET=""
openai.api_key = ""
REDIRECT_URI="https://8080-cs-184908628077-default.cs-us-east1-vpcf.cloudshell.dev/"
PERMISSIONS="user-library-read user-read-recently-played user-read-playback-state"
app.config.update(SECRET_KEY=CLIENT_SECRET)

def get_datastore_client():
    return datastore.Client()

def get_storage_client():
    return storage.Client()

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
    # set the datastore and the storage clients
    datastoreClient = get_datastore_client()
    storageClient = get_storage_client()

    # dummy data for demonstration purposes - we will get this data from the spotify api
    username = "testuser1"
    favGenre = 'rock'
    imageUrl = 'https://cdn.discordapp.com/attachments/1024113488483864669/1033931366573805568/unknown.png'
        
    # NOTE: upload code will be moved to the image generation route of the api

    # uploading to datastore
    newkey = datastoreClient.key('SpotifyUser', username)
    spotifyUser = datastore.Entity(key = newkey)
    spotifyUser['username'] = username
    spotifyUser['imagePath'] = '/images/' + username
    spotifyUser['favGenre'] = favGenre
    datastoreClient.put(spotifyUser)

    # uploading the image to the cs1520moodify.appspot.com bucket
    imageRequest = requests.get(imageUrl)

    userImage = Image.open(BytesIO(imageRequest.content))
    userImage.show()

    fs = FileStorage()

    userImage.save(fs, 'png')

    Image.open(fs).show()

    bucket = storageClient.bucket("cs1520moodify.appspot.com")
    # source_file_name = imageUrl
    blob = bucket.blob("images/" + username + ".png")

    fs.seek(0)
    blob.upload_from_file(fs)    

@app.route('/api/images')
def fetchImages():
    # set the datastore and the storage clients
    datastoreClient = get_datastore_client()
    storageClient = get_storage_client()

    # dummy data for demonstration purposes - we will get this data from the spotify api
    username = "testuser1"
    favGenre = 'rock'
    imageUrl = 'https://cdn.discordapp.com/attachments/1024113488483864669/1033931366573805568/unknown.png'
    
    # NOTE: upload code will be moved to the image generation route of the api

    # uploading to datastore
    newkey = datastoreClient.key('SpotifyUser', username)
    spotifyUser = datastore.Entity(key = newkey)
    spotifyUser['username'] = username
    spotifyUser['imagePath'] = '/images/' + username
    spotifyUser['favGenre'] = favGenre
    datastoreClient.put(spotifyUser)

    

    # uploading the image to the cs1520moodify.appspot.com bucket
    imageRequest = requests.get(imageUrl)

    userImage = Image.open(BytesIO(imageRequest.content))
    userImage.show()

    fs = FileStorage()

    userImage.save(fs, 'png')

    Image.open(fs).show()

    bucket = storageClient.bucket("cs1520moodify.appspot.com")
    # source_file_name = imageUrl
    blob = bucket.blob("images/" + username + ".png")

    fs.seek(0)
    blob.upload_from_file(fs)





    # Uploading data

    # database addition logic
    # user_info = sp.me() - retrieve user info (also could use sp.current_user())
    # username = user_info['display_name']
    # we could use the username as the entity's ID for future retrieval
    # client = get_client()
    # newkey = client.key('SpotifyUser', username)
    # spotifyuser = datastore.Entity(key = newkey)
    # spotifyuser['username'] = username
    # spotifyuser['imagePath'] = 
    # spotifyuser['favGenre'] = 
    # client.put(spotifyuser)

    # Retrieving data
    
    query = datastoreClient.query(kind = "SpotifyUser")
    #basically just fetches every user entity, note we can use limit = n in the query.fetch() 
    #                                   call to set a cap on how many images we display
    
    results = list(query.fetch())
    imageList = []

    for user in results:
        # print(user["imageUrl"])
        imageList.append(user["imagePath"])

    # print(urlList)
    
    return jsonify({
      'imagePath' : imageList
    })

    #return jsonify({
    #    'imageUrl' : ['https://cdn.discordapp.com/attachments/1024113488483864669/1033931366573805568/unknown.png', 'https://cdn.discordapp.com/attachments/1024113488483864669/1033931000260083743/unknown.png']
    #})    

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


