import OpenAiSetUp
import openai 
import os

openai.api_key = "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"
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





# openai.api_key = os.getenv("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")

# prompt = ("Escribe un artículo sobre las zapatillas Air Jordan")

# response = openai.Completion.create(
#      engine="text -davinci-02",
#      prompt=prompt,
#      temperature=0.7,
#      max_tokens=300
#  )

# print(response)

