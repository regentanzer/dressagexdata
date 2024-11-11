import sqlite3
import pandas as pd

conn = sqlite3.connect('dressage.db')
test_results = pd.read_sql_query("SELECT * FROM test_results", conn)
movement_results = pd.read_sql_query("SELECT * FROM movement_results", conn)

def descriptive_stats(df):
    print("Descriptive Stats:")
    print(df.describe())

descriptive_stats(test_results)


conn.close()