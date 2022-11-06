from operator import is_
import time
from flask import Flask, request, json, session, redirect, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

CLIENT_ID=""
CLIENT_SECRET=""
REDIRECT_URI="http://localhost:3000"
PERMISSIONS="user-library-read"
app.config.update(SECRET_KEY=CLIENT_SECRET)
sp_oauth = SpotifyOAuth( CLIENT_ID, CLIENT_SECRET,REDIRECT_URI,scope=PERMISSIONS,cache_path='.spotipyoauthcache' )

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

def check_token():
    token_info = session.get('token_info', None)
    if not token_info:
        raise 'exception'
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

@app.route('/getPrompt', methods=['GET'])
def get_prompt():
    token_info = check_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
    return results