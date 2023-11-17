
from mailjet_rest import Client
from  openai import OpenAI 
import json 

def sendEmail(message,data):
  api_key = data["EMAIL_API_KEY"]
  api_secret = data["EMAIL_SECRET_KEY"]
  mailjet = Client(auth=(api_key, api_secret), version='v3.1')
  data = {
    'Messages': [
      {
        "From": {
          "Email": "adowning@bottom-feeders.com",
          "Name": "Aaron "
        },
        "To": [
          {
            "Email": "{}".format(message['email']),
            "Name": "Aaron "
          }
        ],
        "Subject": "Greetings from Mailjet.",
        "TextPart": "{}".format(message['message']),
        #"HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
        "CustomID": "AppGettingStartedTest"
      }
    ]
  }
  result = mailjet.send.create(data=data)
  print(result.status_code)
  print(result.json())

  return "email has been sent successfully"
    

def analyze_image(message,data):
   print(message["message"].replace("<img src=","").replace(">","").replace("'",""))
   client = OpenAI(api_key=data["API_KEY"])
   completion = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "What’s in this image?"},
            {
              "type": "image_url",
              "image_url": {
                "url": message["message"].replace("<img src=","").replace(">","").replace("'",""),
              },
            },
          ],
        }
      ],
      max_tokens=300,
    )
   return completion.choices[0].message.content
    
   
    