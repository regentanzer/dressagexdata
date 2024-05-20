
import sqlite3
import csv
import os

#######↓ Change the parameters here ↓#######
dbname = 'C:\\Users\\regen\\Documents\\Python\\dressage_database.sqlite'
target_table_name = 'overall_results'
import_table_name = 'C:\\Users\\regen\\Documents\\Python\\DressageTests\\rawfiles\\overall_results.tsv'
is_create_table = True
is_header_skip = True
#####################################


#######↓ Import destination table DDL ↓#######
sql_script = """
CREATE TABLE overall_results (
overall_results_id int,
show_id int,
show_test_id int,
test_id int,
horse_id int,
judge_id int,
judge_rating varchar(50),
test_datetime datetime,
points_earned int,
gaits_mark int,
impulsion_mark int,
submission_mark int,
rider_mark int,
rider_position_mark int,
rider_effectiveness_mark int,
rider_harmony_mark int,
overall_comments varchar(2500)
);
"""
#######################################

class ImportSQLite():
    def __init__(self, dbname, target_table_name, import_data_name, is_create_table, is_header_skip=False, sql_create_table=None):
        """
        Import csv or tsv files into SQLite
        :param dbname:text Connection destination DB name
        :param target_table_name:text Table name on the DB to be imported
        :param import_data_name:text The name of the data you want to import
        :param is_create_table:boolean Whether to create a table to import to
        :param is_header_skip:boolean Whether to skip the header of the data to be imported
        :param sql_create_table:text DDL of the table to be imported
        """
        self.dbname = dbname
        self.target_table_name = target_table_name
        self.import_data_name = import_data_name
        self.is_create_table = is_create_table
        self.is_header_skip = is_header_skip
        _, raw_delimiter = os.path.splitext(import_data_name)
        if raw_delimiter == '.csv':
            self.delimiter = ','
        elif raw_delimiter == '.tsv':
            self.delimiter = '\t'
        else:
            raise ValueError('Import file should be csv or tsv.')

        if is_create_table:
            if not sql_create_table:
                raise ValueError('It\'s necessary of sql to create table')
            else:
                self.sql_create_table = sql_create_table

    def read_import_file(self):
        with open(self.import_data_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            if self.is_header_skip:
                header = next(reader)

            return [i for i in reader]

    def pick_column_num(self, import_data):
        """
Calculate the number of columns in the import file
        :param import_data: array(two-dimensional)
        :return: int
        """
        columns = []
        for raw in import_data:
            columns.append(len(raw))
        if len(set(columns)) == 1:
            return columns[0]
        else:
            raise ValueError('this import files has diffrenect column numbers.')


    def insert_csv_file(self):
        input_file = self.read_import_file()
        column = self.pick_column_num(input_file)
        val_questions = ['?' for i in range(column)]
        cur.executemany("insert into {0} values ({1})".format(self.target_table_name, ','.join(val_questions)), input_file)


if __name__ == '__main__':

    sql = ImportSQLite(
        dbname=dbname,
        target_table_name=target_table_name,
        import_data_name=import_table_name,
        is_create_table=True,
        is_header_skip= is_header_skip,
        sql_create_table=sql_script
    )

    conn = sqlite3.connect(sql.dbname)
    cur = conn.cursor()

    if sql.is_create_table:
        cur.execute('drop table if exists {};'.format(target_table_name))
        cur.execute(sql.sql_create_table)

    sql.insert_csv_file()

    conn.commit()
    conn.close()


