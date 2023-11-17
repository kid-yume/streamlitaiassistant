#Load openAI library and others 
from  openai import OpenAI 
import json

data ={}
with open("../../config.json", "r") as jsonfile:
    data = json.load(jsonfile)
    
client = OpenAI(api_key="{}".format(data["API_KEY"]))


assistant = client.beta.assistants.create(
  name="Streamlit_AI_Assitant_test",
  instructions="You are a AI assisstant",
  model="gpt-3.5-turbo",
  tools=[{"type": "code_interpreter"}]
)
#Put The ID in your config.json Saving it for ya ^_^
print(assistant.id)
with open("../../config.json", "r+") as jsonFile:
    data = json.load(jsonFile)

    data["ASSITANT_ID"] = "{}".format(assistant.id)
    jsonFile.seek(0)  # rewind
    json.dump(data, jsonFile,indent=4, sort_keys=True)
    jsonFile.truncate()

my_updated_assistant = client.beta.assistants.update(
  assistant.id,
  instructions="You are a helpful assistant. Reply TERMINATE when the task is done.",
  name="Streamlit Helper",
  tools=[{
    "type": "function",
    "function": {
      "name": "ask_image_analyzer",
      "description": "ask image analyzer when an image needs to be analyzed",
      "parameters": {
        "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "details needed from the image. Ensure the task includes the actual image and the message contains the image location for example \"<img fileLocation>\" and enough context, such as the information that needs to be extracted from the image be sure the location is wrapped in an image tag. For example <img /folderlocation/file.jpg>. The image analyzer does not know the conversation between you and the user unless you share the conversation with the expert. Save to a txt file.",
                }
            },
            "required": ["message"],
        }
    }
  },
  {
   "type": "function",
    "function":{
        "name": "send_email",
        "description": "When an email needs to be sent to a desired receipient use this function",
        "parameters": {
            "type": "object",
            "properties": {
            "message": {
                "type": "string",
                "description": "This is the content of the email. Include whatever the user wishes to communicate here "
            },
            "email": {
                "type": "string",
                "description": "This is the email address of the person that will be receiving the message."
            }
            },
            "required": [
            "message",
            "email"
            ]
        }
    } 
    }],
  model="gpt-3.5-turbo",
  
)

print("Complete")
#print the AI Assistant ID and save it 