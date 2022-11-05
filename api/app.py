from operator import is_
from flask import Flask, request, url_for, session, redirect, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

app.secret_key = "19u2h31289ias" # this is random, ignore for now.
app.config['SESSION_COOKIE_NAME'] = 'test cookie'
TOKEN_INFO = 'token_info'

@app.route('/authorize')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return jsonify({
        'auth_endpoint': auth_url
    })

@app.route('/sentence', methods=['GET'])
def get_top_songs_genre(song_ids, artist_ids, token_info):
        
    sp = spotipy.Spotify(auth=token_info['access_token'])

    genres = sp.recommendation_genre_seeds()
    refined_genres = sp.recommendations(song_ids, artist_ids, genres, limit=1)
    example_string = refined_genres + " abstract" + " digital art"
    return str(example_string)

def create_spotify_oauth():
    # ENTER YOUR OWN CLIENT ID AND SECRET FROM THE SPOTIFY DASHBOARD
    return SpotifyOAuth(
        client_id='',
        client_secret='',
        redirect_uri='http://localhost:3000',
        scope='user-library-read'
    )

# make sure to delete client secret and client id before uploading to Github or anywhere public
# https://app-engine-react-demo-dot-cs1520-jel211.ue.r.appspot.com/