
from  openai import OpenAI 
from Monitor.openaifolder.functioncalls import sendEmail,analyze_image
import json 




def executeRun(runid,threadid,dbm):
    data={}
    with open("../../config.json", "r") as jsonfile:
        data = json.load(jsonfile)
        print("Read successfully")
        print(data)
    client = OpenAI(api_key=data["API_KEY"])
    functionsToUse = {'send_email':sendEmail, 'ask_image_analyzer':analyze_image}
    run= client.beta.threads.runs.retrieve(
        run_id=runid,
        thread_id=threadid
    )
    tools_calls=[]
    if run.status == "requires_action":
       for tool in run.required_action.submit_tool_outputs.tool_calls:
          print(tool.function.name)
          print(json.loads(tool.function.arguments)["message"])
          tools_calls.append({"tool_call_id":tool.id,"output":functionsToUse[tool.function.name](json.loads(tool.function.arguments),data)})
       run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=threadid,
        run_id=runid,
        tool_outputs=tools_calls
      )
    if run.status =="completed":
      print("now deleteing")
      dbm.ExecuteInsert("DELETE FROM RUNS where ID ='{}'".format(run.id))