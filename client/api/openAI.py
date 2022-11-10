import OpenAiSetUp
import openai 
import os

openai.api_key = ""
# personal key

prompt = "say this is a test"

# Api: Image penerations 
# https://beta.openai.com/docs/guides/images/introduction

response = openai.Image.create(
  prompt="a white siamese cat",
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']



print (response)