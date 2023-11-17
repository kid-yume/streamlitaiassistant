import sqlite3,os,json
from utilities.queries import THREAD_QUERY,RUN_QUERY,CREATE_THREAD_TABLE,CREATE_RUN_TABLE
import pandas as pd 

class DatabaseManager:
    def __init__(self)-> None:
        data={}
        with open("./config.json", "r") as jsonfile:
            data = json.load(jsonfile)
            print("Read successful")
            print(data)
        self.conn = sqlite3.connect(data["DATABASE_NAME"])
        self.curser_obj=self.conn.cursor()
        self.ExecuteInsert(CREATE_THREAD_TABLE)
        self.ExecuteInsert(CREATE_RUN_TABLE)

    def ExecuteInsert(self,query):
        self.curser_obj.execute(query)
        self.conn.commit()
    
    def ExecuteQuery(self,query):
        return pd.read_sql(query ,self.conn)
    
    def CloseConnection(self):
        self.conn.close()
