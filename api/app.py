from operator import is_
from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google.cloud import datastore
import time

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

@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print('user not logged in')
        return redirect('/')
        
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return str(sp.current_user_saved_tracks(limit=50, offset=0)['items'])

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
        client_id='',
        client_secret='',
        redirect_uri=url_for('redirectPage', _external=True),
        scope='user-library-read'
    )
# make sure to delete client secret and client id before uploading to Github or anywhere public
# https://app-engine-react-demo-dot-cs1520-jel211.ue.r.appspot.com/