import json
import csv
import os
import mysql.connector
import sys
import psycopg2
from interface import implements, Interface
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from  parse import *
import datetime

class ISqlRawGetter(Interface):

    def get_table_raw(self, table_name, i, cursor=None):
        pass

    def get_cursor(self, **kwargs):
        pass

class SqlConnection():
    def __init__(
        self, host,
        user, password,
        database, charset=None):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database)

    def get_table_fields(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute("Select * FROM %s where id = 0" % (table_name,))
        return [desc[0] for desc in cursor.description]

    def get_table_length(connection, table_name):
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) from %s" % (table_name,));
        return cursor.fetchone()[0]

class MySqlConnection(SqlConnection, implements(ISqlRawGetter)):
    def __init__(self, host, user, password, database):
        super().__init__(
            host = host, user = user,
            password = password, database = database)

    def get_table_raw(self, table_name, i, cursor = None):
        if cursor == None:
            cursor = self.get_cursor()
        cursor.execute('SELECT * FROM %s where id= %d' % (table_name, i))
        try:
            fetched = cursor.fetchall()
            fetched  = fetched[0]
            return fetched
        except:
            print (i)
            print (fetched)

    def get_cursor(self, **kwargs):
        print("kwargs : ", kwargs)
        if (len(kwargs) == 0):
            return self.connection.cursor(dictionary=True,
                              buffered=False)
        else:
            return self.connection.cursor(**kwargs)

    def select_text_by_id(self, table_name, i, key, cursor = None):
        if cursor == None:
            cursor = self.get_cursor()
        try:
            return get_table_raw[key]
        except:
            return ''

def json2csv():
    in_file = open(file_path, 'r')
    if not out_file_path:
        out_file_path = os.path.join(
            os.getcwd(),
            os.path.split(file_path)[-1].split('.')[0] + ".csv")
        if os.path.exists(out_file_path):
            print("file %s already exists. Specify path to the file" % (out_file_path,))
    json_file = json.load(in_file)
    for row in json_file:
        column_names = sorted(row.keys())
        csv_writer = csv.DictWriter(
                open(out_file_path, 'w'),
                fieldnames=column_names,
                delimiter='\t')
        break
    for row in json_file:
        csv_writer.writerow(row)

def sql2csv(
        host, user, password,
        database, table_name, out_file_path):

        sql_converter  = MySqlConnection(
            host=host,
            user=user,
            password=password,
            database=database)
        print("TABLE NAME :",table_name, "len", len(table_name))

        csv_writer = csv.DictWriter(
                open(out_file_path, 'w'),
                 fieldnames =  sql_converter.get_table_fields(table_name),
                delimiter='\t')
        cursor = sql_converter.get_cursor(
            buffered=False,
            dictionary=True)
        csv_writer.writeheader()
        for i in range(1, sql_converter.get_table_length(table_name)

                           ):

                        raw = sql_converter.get_table_raw(table_name, i, cursor)
                        if raw:
                            print (i)
                            csv_writer.writerow(raw)

if __name__=='__main__':
    #json_to_csv('./data/tonality/test.json')
    '''db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="ASSANGE",
        database="pscraper",
        charset="utf8")'''
    sql2csv(
        host="localhost",
        user="root",
        password="root",
        database="bel_sites",
        table_name='publications',
        out_file_path='publications.csv')
