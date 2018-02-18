#!/usr/bin/python3
import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ASSANGE",
    database="amazon_db",
    charset="utf8")
cursor = db.cursor(buffered=False, dictionary=True)

cursor.execute("USE amazon_db") # select the database
cursor.execute("SHOW TABLES")
print(cursor.fetchall())

cursor.execute('select * from publications where id = 10001')
print(cursor.fetchall()[0]['content'])
