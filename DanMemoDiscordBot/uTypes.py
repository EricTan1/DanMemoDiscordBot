import json
import os
import sys
from urllib.parse import urlparse
import mysql.connector

path = "./unitTypes"
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="danmemo", port=3306, database="danmemo")
mycursor = connection.cursor()

#db = DBcontroller(HOSTNAME,USERNAME,PASSWORD,"3306",DATABASE)
for filename in os.listdir(path):
    with open(path + '/' + filename, 'r', encoding="utf8") as f:
        
        unitType = filename.replace(".txt","")
        if(unitType == "Balance"):
            type_id = 62
        elif(unitType == "Defensive"):
            type_id = 68
        elif (unitType == "Healer"):
            type_id = 67
        #print(alias_name)
        line = f.readline()
        while(line):
            
            temp_line = line.strip()
            if(temp_line != "" and temp_line != "\n"):
                sql = 'UPDATE danmemo.adventurer SET typeid = "{}" WHERE title="{}";'.format(type_id,temp_line)
                mycursor.execute(sql)
                connection.commit()
               

            line = f.readline()
