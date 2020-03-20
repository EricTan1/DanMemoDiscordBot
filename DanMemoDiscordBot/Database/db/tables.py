import mysql.connector

from urllib.parse import urlparse


result = urlparse("mysql://bdcaa58f136231:c268bc42@us-cdbr-iron-east-04.cleardb.net/heroku_0fe8a18d3b21642?reconnect=true")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

print(username)
print(password)
print(database)
print(hostname)

connection = mysql.connector.connect(
    database = database,
    user = username,
    password = password,
    host = hostname
)
cursor = connection.cursor()



f = open("./danmemo_type.sql", "r")
mysql = f.read()
#cursor.execute("show tables;")
cursor.execute(mysql)
#connection.commit()
for row in cursor: 
    print(row)

f.close()
cursor.close()
connection.close()