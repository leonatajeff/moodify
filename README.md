# moodify
We are developing a web app inspired by https://receiptify.herokuapp.com/ in GAE and Flask for CS1520. 

## Cloud datastore
Our data will be stored with google datastore.

1) Configure your project to cs1520moodify
2) Start the development server
3) Initialize the environment

```bash
$ gcloud config set project cs1520moodify
$ gcloud beta emulators datastore start &
$ $(gcloud beta emulators datastore env-init)
```


## ⛷ Run the backend
For our development phase, you must add your client id and secret from the spotify dashboard for the API to work. We do not have dynamic login yet.

```bash
$ cd api
$ flask run
```

## ⛷ Run the frontend

```bash
$ cd client
$ npm run start
```