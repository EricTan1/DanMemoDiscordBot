import json
import os
import sys
from urllib.parse import urlparse
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="danmemo", port=3306, database="danmemo")
mycursor = connection.cursor()

#db = DBcontroller(HOSTNAME,USERNAME,PASSWORD,"3306",DATABASE)
with open('HeroAscendable.txt', 'r', encoding="utf8") as f:
    #print(alias_name)
    line = f.readline()
    while(line):
        temp_line = line.strip()
        print(temp_line)
        if(temp_line != "" and temp_line != "\n"):
            sql = 'UPDATE danmemo.adventurer SET ascended = "{}" WHERE title="{}";'.format(1,temp_line)
            mycursor.execute(sql)
            connection.commit()
            

        line = f.readline()
