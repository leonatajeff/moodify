# moodify
We are developing a web app inspired by https://receiptify.herokuapp.com/ in GAE and Flask for CS1520. 

# Setting up the production environment:

## GAE

```bash
$ dev_appserver.py app.yaml
```

## Cloud datastore
Our data will be stored with google datastore.

1) Configure your project to cs1520moodify

```bash
$ gcloud config set project cs1520moodify
```


# Setting up the local development

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
