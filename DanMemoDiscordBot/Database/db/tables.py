import psycopg2

from urllib.parse import urlparse


result = urlparse("postgres://kbkuvsqpfvseag:7518c50d4ccd8f087674ccc1f62be0b43118950f54f5cdbe5af1ebc31cf364b0@ec2-54-75-235-28.eu-west-1.compute.amazonaws.com:5432/d16efjkhav7kre")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

print(username)
print(password)
print(database)
print(hostname)

connection = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname
)
cursor = connection.cursor()
f = open("./danmemo_type.sql", "r")
print(my_sql)

cursor.execute(my_sql)
#cursor.commit()
rows = cursor.fetchall()
for row in rows:
    print("   ", row)

cursor.close()
connection.close()