import json
import csv
import os
import mysql.connector
import sys
import psycopg2
import psycopg2.extras
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
        pass

    def get_table_fields(self, table_name):
        self.cursor.execute("Select * FROM %s where id = 0" % (table_name,))
        return [desc[0] for desc in self.cursor.description]

    def get_table_length(self, table_name):
        cursor = self.connection.cursor(buffered = True)
        cursor.execute("SELECT COUNT(*) from %s" % (table_name,));
        return cursor.fetchone()[0]

    def get_table_raw(self, table_name, i, cursor = None):
        if cursor is None:
            cursor = self.get_cursor()
        cursor.execute('SELECT * FROM %s where id= %d' % (table_name, i))
        try:
            fetched = cursor.fetchall()
            fetched = fetched[0]
            return fetched
        except:
            print (i)
            print (fetched)

    def select_field_by_id(self, table_name, i, key):
        try:
            return self.get_table_raw(
                table_name=table_name, i=i)[key]
        except:
            return ''

class _MySqlConnection(SqlConnection, implements(ISqlRawGetter)):
    def __init__(self, host, user, password, database):
        super().__init__(
            host = host, user = user,
            password = password, database = database)

        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database)
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)

    def get_cursor(self, **kwargs):
        print("kwargs : ", kwargs)
        if (len(kwargs) == 0):
            return self.connection.cursor(
                dictionary=True,
                buffered=False)
        else:
            return self.connection.cursor(**kwargs)

class PostgresSqlConnecton(SqlConnection, implements(ISqlRawGetter)):
    def __init__(self, host, user, password, database):
        super().__init__(
            host=host, user=user,
            password=password, database=database)

        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database)
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

    def get_cursor(self, **kwargs):
        print("kwargs : ", kwargs)
        if (len(kwargs) == 0):
            return self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            return self.connection.cursor(**kwargs)


'''def json2csv():
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
        csv_writer.writerow(row)'''

def sql2csv(
    host, user, password,
    database, table_name, out_file_path):
        sql_converter  = _MySqlConnection(
            host=host,
            user=user,
            password=password,
            database=database)
        print("TABLE NAME :",table_name, "len", len(table_name))
        csv_writer = csv.DictWriter(
                open(out_file_path, 'w'),
                 fieldnames =  sql_converter.get_table_fields(table_name),
                delimiter='\t')
        '''cursor = sql_converter.get_cursor(
            buffered=False,
            dictionary=True)'''
        csv_writer.writeheader()
        for i in range(1, sql_converter.get_table_length(table_name)):
            raw = sql_converter.get_table_raw(table_name, i)
            if raw:
                # print (i)
                csv_writer.writerow(raw)

def get_new_cursor(self, **kwargs):
    print("kwargs : ", kwargs)
    if not len(kwargs):
        return self.cursor(dictionary=True, buffered=False)
    else:
        return self.cursor(**kwargs)

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
        password="ASSANGE",
        database="pscraper",
        table_name="publications",
        out_file_path='contents.csv')
    '''
    lol = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ASSANGE",
        database="pscraper")

    a = get_new_cursor(lol,
        buffered=False,
        dictionary=True)
    print(a)'''
