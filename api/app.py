import time
from flask import Flask, request, json, session, redirect, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google.cloud import datastore
# from google.cloud import storage

app = Flask(__name__)

CLIENT_ID="606c383fe48b4ba89afc1bdecd6f932f"
CLIENT_SECRET="7a97aff89abe4e0ba98e6401734c24b0"
REDIRECT_URI="http://localhost:3000"
PERMISSIONS="user-library-read"
app.config.update(SECRET_KEY=CLIENT_SECRET)
sp_oauth = SpotifyOAuth( CLIENT_ID, CLIENT_SECRET,REDIRECT_URI,scope=PERMISSIONS,cache_path='.spotipyoauthcache' )

def get_client():
    return datastore.Client()

#def get_storage_client():
#    return storage.Client()

@app.route('/authorize')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return jsonify({
        'auth_endpoint': auth_url
    })

@app.route('/registerToken', methods=['POST'])
def register_token():
    data = json.loads(request.data) 
    token_info = sp_oauth.get_access_token(data['code'])
    session['token_info'] = token_info
    return token_info

@app.route('/images')
def fetchImages():

    client = get_client()
    query = client.query(kind = "SpotifyUser")
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

@app.route('/getPrompt', methods=['GET'])
def get_prompt():
    try:
        token_info = check_token()
    except:
        print('user not logged in')
        return redirect('/')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
    return results

@app.route('/prompt', methods=['GET'])
def get_prompts():
    try:
        token_info = check_token()
    except:
        print('user not logged in')
        return redirect('/')
        
    user_track_info = get_user_top_tracks(token_info)
    # Parsing through the API call for specific data to get genres
    id_top_track = user_track_info.get("song_id")
    uri_top_artist = user_track_info.get("artist_uri")


    genres = get_top_songs_genre(id_top_track, uri_top_artist, token_info)

    #top_track_features = get_audio_feature(id_top_track)
    #gen_string = image_gen_string(top_track_features, song_top_track, artist_top_track)
    return genres
   
def check_token():
    token_info = session.get('token_info', None)
    if not token_info:
        raise Exception("Token error")
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

'''
    Logic for data from Spotify
    I am not too sure how to connect this to the front-end
    I can do redirect in js but not python.... oops 
    We probably dont have to refine anything crazy until milestone 3
    For now I will provide strings for the users top track and create strings from that piece of data

'''
def get_user_top_tracks(token_info):
    '''
        Gets the user top tracks based on query from endpoint.
        For limit, offset, time_range... I will make cleaner query variable to adjust 
        without changing link manaully
    '''
        
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    resp_json = sp.current_user_top_tracks(limit=5, offset=0, time_range='medium_term')
    
    # Parsing the user's top 5 tracks 
    list_of_results = resp_json['items']
    list_artist_names   = [] # list of artist names
    list_song_names     = [] # list of top song names
    list_song_ids       = [] # id of the song to use for further data e.g) audio_features endpoint
    list_artist_uri     = [] # artist's resource identifier in Spotify's database

    for result in list_of_results:
        curr_artist = result['album']['artists'][0]['name']
        curr_song = result['name']
        curr_id = result['album']['artists'][0]['id']
        curr_artist_uri = result['album']['artists'][0]['uri']
        list_artist_names.append(curr_artist)
        list_song_names.append(curr_song)
        list_song_ids.append(curr_id)
        list_artist_uri.append(curr_artist_uri)

    '''
        I will probably restructure this... ?
        Looks like this: 
            {
                song: [song1,song2,song3,song4],
                artist: [artistOfSong1, artistOfSong2, artistOfSong3, artistOfSong4],
                song_id: [idOfSong1, idOfSong2, idOfSong3, idOfSong4],
                artist_uri: [uri1, uri2, uri3, uri4]
            }    
    '''
    top_track_info = {
        "song": list_song_names,
        "artist": list_artist_names,
        "song_id": list_song_ids,
        "artist_uri": list_artist_uri
    }   

    
    return top_track_info

def get_top_songs_genre(song_ids, artist_ids, token_info):
    '''
    We're . This will generate a list of genres based on songs entered. 

    Genre seeds are just genre titles that spotify uses to generate a set of recommendations
    https://developer.spotify.com/documentation/web-api/reference/#/operations/get-recommendation-genres

    recommendations(seed_artists=None, seed_genres=None, seed_tracks=None, limit=20, country=None, **kwargs)
        Get a list of recommended tracks for one to five seeds. (at least one of seed_artists, seed_tracks and seed_genres are needed)
    recommendation_genre_seeds()
        Get a list of genres available for the recommendations function.
    USE ART MOVEMENTS AND DESCRIPTORS LIKE ABSTRACT, ETC.
    '''
        
    sp = spotipy.Spotify(auth=token_info['access_token'])

    genres = sp.recommendation_genre_seeds()
    refined_genres = sp.recommendations(song_ids, artist_ids, genres, limit=1)
    prompt_string = refined_genres + " abstract" + " digital art"
    return prompt_string

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