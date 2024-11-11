import sqlite3
import pandas as pd

conn = sqlite3.connect('dressage.db')
cursor = conn.cursor()

data_folder = 'raw_test_data/'

def load_tsv_to_sqlite(file_name, table_name):
    df = pd.read_csv(data_folder + file_name, sep='\t')
    df.to_sql(table_name, conn, if_exists='replace', index=False)

load_tsv_to_sqlite('facility.tsv', 'facility')
load_tsv_to_sqlite('horse.tsv', 'horse')
load_tsv_to_sqlite('individual_scores.tsv', 'individual_scores')
load_tsv_to_sqlite('judge.tsv', 'judge')
load_tsv_to_sqlite('overall_results.tsv', 'overall_results')
load_tsv_to_sqlite('show.tsv', 'show')
load_tsv_to_sqlite('test_movements.tsv', 'test_movements')
load_tsv_to_sqlite('test.tsv', 'tests')

conn.commit()
conn.close()

print("Database successfully created!")
