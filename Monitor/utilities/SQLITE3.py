import pyodbc
import json 
import pandas as pd
import sqlite3


class SQLLITEDatabaseManagerOther:
    def __init__(self)-> None:
        with open("../../config.json", "r") as jsonfile:
            data = json.load(jsonfile)
        self.conn = sqlite3.connect(data["DATABASE_NAME"])
        self.curser_obj=self.conn.cursor()
    
    def ExecuteInsert(self,query):
        self.curser_obj.execute(query)
        self.conn.commit()


    
    def ExecuteQuery(self,query):
        return pd.read_sql(query ,self.conn)


