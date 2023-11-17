from  openai import OpenAI 
from Monitor.utilities.SQLITE3 import SQLLITEDatabaseManagerOther
from Monitor.openaifolder.openairunfunctions import executeRun
import time,json

data={}
with open("../config.json", "r") as jsonfile:
    data = json.load(jsonfile)

client = OpenAI(api_key=data["API_KEY"])
dbm = SQLLITEDatabaseManagerOther()

RUN_QUERY="SELECT * FROM RUNS;"
RUN_QUERY_DELETE="DELETE FROM RUNS where id = '{RUNID}';"
RUN_QUERY_DELETE="DELETE FROM THREADS"
while True:
    if len(dbm.ExecuteQuery(RUN_QUERY)) > 0:
      for run in dbm.ExecuteQuery(RUN_QUERY).values:
         print(run[0])
         executeRun(run[0],run[1],dbm)
    else:
       time.sleep(3)
       pass