# moodify
We are developing a web app inspired by https://receiptify.herokuapp.com/ in GAE and Flask for CS1520. 

# Setting up the GAE-Hosted Environment:

## Cloud datastore
To properly interact with any server data, ensure the project is set to the `cs1520moodify` cloud instance.

```bash
$ gcloud config set project cs1520moodify
```

## GAE

1) Set up CLIENT_ID and CLIENT_SECRET in main.py (a more secure way to store keys and secrets will be implemented soon)
1) In your terminal, go to `/client/` folder

Run below CLI commands
```bash
$ npm i
$ npm run create-deployable
$ cd api
$ dev_appserver.py app.yaml
```
2) Open web preview. 
- Add a url to the redirect uri(s) in your spotify dashboard.
- Set the url to the redirect uri in `main.py`


# Setting up the local development environment

## ⛷ Running the backend
For our development phase, you must add your client id and secret from the spotify dashboard for the API to work. Also depending on your development environment, you must add the appropriate redirect URIs (where can Spotify.com go after verification?) 

[Example of a Spotify Redirect URI List](https://user-images.githubusercontent.com/42332446/200457221-f1236cea-b44a-4050-adf6-7513b8d10963.png)

```bash
$ cd api
$ python3 setup.py install
$ flask run
```

## ⛷ Running the frontend

```bash
$ cd client
$ npm install
$ npm run start
```

- [Milestone 1](https://youtu.be/dSuuu2swJ7s)
- [Milestone 2](https://www.youtube.com/watch?v=nW4ZB0cE-kU&ab_channel=JeffersonLeonata)
