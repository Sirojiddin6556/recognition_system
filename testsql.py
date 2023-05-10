import sqlite3

connection = sqlite3.connect('people.db')
crsr = connection.cursor()
sql_command = """CREATE TABLE registration (
id INTEGER PRIMARY KEY,
numb VARCHAR(30),
name VARCHAR(30),
datetime DATATIME)"""
crsr.execute(sql_command)
connection.close()

