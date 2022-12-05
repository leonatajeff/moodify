from google.cloud import datastore
from google.cloud import storage
import requests
from werkzeug.datastructures import FileStorage 
from PIL import Image
from io import BytesIO
from flask import jsonify

def get_datastore_client():
    return datastore.Client()

def get_storage_client():
    return storage.Client()


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


def upload(username, favGenre, prompt, imageUrl):
    # set the datastore and the storage clients
    datastoreClient = get_datastore_client()
    storageClient = get_storage_client()

    # uploading to datastore
    newkey = datastoreClient.key('SpotifyUser', username)
    spotifyUser = datastore.Entity(key = newkey)

    imageName = str(newkey.id)

    spotifyUser['username'] = username
    spotifyUser['imagePath'] = '/images/' + imageName + '.png'
    spotifyUser['favGenre'] = favGenre
    spotifyUser['prompt'] = prompt
    datastoreClient.put(spotifyUser)

    # uploading the image to the cs1520moodify.appspot.com bucket
    imageRequest = requests.get(imageUrl)

    userImage = Image.open(BytesIO(imageRequest.content))

    fs = FileStorage()

    userImage.save(fs, 'png')

    bucket = storageClient.bucket("cs1520moodify.appspot.com")
    # source_file_name = imageUrl
    blob = bucket.blob("images/" + imageName + ".png")

    fs.seek(0)
    blob.upload_from_file(fs)    

def getImages():
    # Retrieving data

    datastoreClient = get_datastore_client()
    
    query = datastoreClient.query(kind = "SpotifyUser")
    #basically just fetches every user entity, note we can use limit = n in the query.fetch() 
    #                                   call to set a cap on how many images we display
    
    results = list(query.fetch())
    imageList = []

    for user in results:
        imageList.append(user["imagePath"])
    
    ## we will probably have to add more here for whatever other info we want to display
    # maybe another list with prompts, maybe another with favorite genres, etc. 
    
    return jsonify({
      'imagePath' : imageList
    })


