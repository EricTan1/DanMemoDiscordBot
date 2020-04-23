import json
import os
import sys
from urllib.parse import urlparse
import mysql.connector

path = "./characterAliases"
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="danmemo", port=3306, database="danmemo")
mycursor = connection.cursor()

#db = DBcontroller(HOSTNAME,USERNAME,PASSWORD,"3306",DATABASE)
for filename in os.listdir(path):
    with open(path + '/' + filename, 'r', encoding="utf8") as f:
        alias_name = filename.replace(".txt","")
        #print(alias_name)
        line = f.readline()
        while(line):
            
            temp_line = line.strip()
            if(temp_line != "" and temp_line != "\n"):
                temp_alias = "null"
                #adventurer
                alias_sql = 'SELECT alias FROM danmemo.adventurer WHERE title="{}";'.format(temp_line)
                mycursor.execute(alias_sql)
                
                for row in mycursor:
                    temp_alias =row[0]
                #assist
                #alias_sql = 'SELECT alias FROM danmemo.assist WHERE title="{}";'.format(temp_line)
                #mycursor.execute(alias_sql)
                
                #for row in mycursor:
                    #temp_alias =row[0]
                
                print(temp_line)
                print(temp_alias)
                if(not(alias_name.lower() in temp_alias)):
                    if(temp_alias == "None"):
                        sql = 'UPDATE danmemo.adventurer SET alias = "{}" WHERE title="{}";'.format(alias_name,temp_line)
                        mycursor.execute(sql)
                        connection.commit()
                    elif(temp_alias != "null"):
                        sql = 'UPDATE danmemo.adventurer SET alias = "{}" WHERE title="{}";'.format(temp_alias+"_"+alias_name,temp_line)
                        mycursor.execute(sql)
                        connection.commit()

            line = f.readline()
