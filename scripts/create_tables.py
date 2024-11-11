import sqlite3

conn = sqlite3.connect('dressage.db')
cursor = conn.cursor()

with open('scripts/create_tables.sql', 'r') as file:
    sql_script = file.read()

cursor.executescript(sql_script) 
conn.commit()  
conn.close()
