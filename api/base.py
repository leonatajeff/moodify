from flask import Flask

api = Flask(__name__)


@api.route('/')
def my_profile():
    response_body = {
        "name": "Jeff",
        "about" :"This is a test response"
    }

    return response_body

@api.route('/authorize')
def authorize():
  client_id = api.config['CLIENT_ID']
  redirect_uri = api.config['REDIRECT_URI']
  scope = api.config['SCOPE']
  state_key = createStateKey(15)
  session['state_key'] = state_key

  authorize_url = 'https://accounts.spotify.com/en/authorize?'
  params = {'response_type': 'code', 'client_id': client_id,
            'redirect_uri': redirect_uri, 'scope': scope, 
            'state': state_key}
  query_params = urlencode(params)
  response = make_response(redirect(authorize_url + query_params))
  return response

def getToken(code):
  token_url = 'https://accounts.spotify.com/api/token'
  authorization = app.config['AUTHORIZATION']
  redirect_uri = app.config['REDIRECT_URI']
  headers = {'Authorization': authorization, 
             'Accept': 'application/json', 
             'Content-Type': 'application/x-www-form-urlencoded'}
  body = {'code': code, 'redirect_uri': redirect_uri, 
          'grant_type': 'authorization_code'}
  post_response = requests.post(token_url,headers=headers,data=body)
  if post_response.status_code == 200:
    pr = post_response.json()
    return pr['access_token'], pr['refresh_token'], pr['expires_in']
  else:
    logging.error('getToken:' + str(post_response.status_code))
    return None

if __name__ == '__main__':
    api.run(host='127.0.0.1', port=8080, debug=True)