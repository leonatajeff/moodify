from operator import is_
from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google.cloud import datastore
import time
from pprint import pprint #pretty print for debugging

SPOTIFY_GET_TOP_TRACKS_URL = 'https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=20&offset=5'

app = Flask(__name__)

app.secret_key = "19u2h31289ias" # this is random, ignore for now.
app.config['SESSION_COOKIE_NAME'] = 'test cookie'
TOKEN_INFO = 'token_info'

def get_client():
    return datastore.Client()

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

# @app.route('/getTracks')
# def getTracks():
#     try:
#         token_info = get_token()
#     except:
#         print('user not logged in')
#         return redirect('/')
        
#     sp = spotipy.Spotify(auth=token_info['access_token'])
    
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


    #return str(sp.current_user_saved_tracks(limit=50, offset=0)['items'])

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise 'exception'
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    # ENTER YOUR OWN CLIENT ID AND SECRET FROM THE SPOTIFY DASHBOARD
    return SpotifyOAuth(
        client_id='3b6e32674826411e982c1e646be333fc',
        client_secret='5e393a79e3964f67a424a680efc9419b',
        redirect_uri=url_for('redirectPage', _external=True),
        scope='user-library-read'
    )
# make sure to delete client secret and client id before uploading to Github or anywhere public
# https://app-engine-react-demo-dot-cs1520-jel211.ue.r.appspot.com/

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


    #parse data 
    list_of_results = resp_json['items']
    list_artist_names   = [] #list of artists for the top songs
    list_song_names     = [] #list of top songs
    list_song_ids       = [] #id of the song to use for further data e.g) audio_features endpoint
    list_artist_uri     = [] #artist of the song's id

    for result in list_of_results:
        curr_artist = result['album']['artists'][0]['name']
        list_artist_names.append(curr_artist)
        curr_song = result['name']
        list_song_names.append(curr_song)
        curr_id = result['album']['artists'][0]['id']
        list_song_ids.append(curr_id)
        curr_artist_uri = result['album']['artists'][0]['uri']
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

def get_audio_feature(top_track_id):
    '''
        Returns the audio feature data for the users top track
    '''
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    audio_info = sp.audio_features(tracks=[])
    
    return audio_info

def image_gen_string(audio_info, song_title, artist_name):
    '''
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

#def parse_audio_features()
'''
    Clean up and give meaning to certain features.
'''

def get_top_songs_genre(song_ids, artist_ids, token_info):
    '''
        Use the top songs to generate a seed genre. This will generate a list of genres based on songs entered. 

        recommendations(seed_artists=None, seed_genres=None, seed_tracks=None, limit=20, country=None, **kwargs)
            Get a list of recommended tracks for one to five seeds. (at least one of seed_artists, seed_tracks and seed_genres are needed)

        recommendation_genre_seeds()
            Get a list of genres available for the recommendations function.

        USE ART MOVEMENTS AND DESCRIPTORS LIKE ABSTRACT, ETC.
    '''
        
    sp = spotipy.Spotify(auth=token_info['access_token'])

    genres = sp.recommendation_genre_seeds()
    refined_genres = sp.recommendations(song_ids, artist_ids, genres, limit=1)
    example_string = ""
    example_string = refined_genres + " abstract" + " digital art"



    


@app.route('/getTracks')
def main():
    try:
        token_info = get_token()
    except:
        print('user not logged in')
        return redirect('/')
        

    user_track_info = get_user_top_tracks(token_info)
    #TEMP FORMAT GETTING THE SONG ID OF TOP TRACK FOR USER
    id_top_track = user_track_info.get("song_id")
    uri_top_artist = user_track_info.get("artist_uri")
    song_top_track = user_track_info.get("song")
    artist_top_track = user_track_info.get("artist")


    genres = get_top_songs_genre(id_top_track, uri_top_artist, token_info) #passes id of songs and artists

    #THIS IS THE STRING TO PLAY WITH ^^^ GENRES RETURNS A STRING TO GENERATE WITH
    print(genres)

    #top_track_features = get_audio_feature(id_top_track)

    #gen_string = image_gen_string(top_track_features, song_top_track, artist_top_track)
    

#playground
if __name__ == '__main__':
    main()