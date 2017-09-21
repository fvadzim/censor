import json
import csv
import os
import mysql.connector
import sys
import psycopg2
from interface import Interface
print(os.path.realpath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
print(sys.path)
from  parse import *
import datetime

class ISqlConvert(Interface):
    def get_table_fields(connection, table_name):
        pass

    def get_table_length(connection, table_name):
        pass

    def get_table_raw(cursor, table_name, i):
        pass

    def select_text_by_id(connectotion, table, i, key):
        pass


class MysqlConverter(ISqlConvert):

    def get_table_fields(connection, table_name):
        cursor = connection.cursor(buffered=False, dictionary=True)
        cursor.execute("describe %s" % (table_name,));
        typenames=[]
        fieldnames=[]
        for field in cursor.fetchall():
            fieldnames.append(field['Field'])
            typenames.append(field['Type'])
        print(typenames)
        return {'fieldnames' : fieldnames, 'typenames': typenames}

    def get_table_length(connection, table_name):
        cursor = connection.cursor(buffered=False, dictionary=True)
        cursor.execute("SELECT COUNT(*) from %s" % (table_name,));
        return int(cursor.fetchone()['COUNT(*)'])

    def get_table_raw(cursor, table_name, i):
        cursor.execute('SELECT * FROM %s where id= %d' % (table_name, i))
        try:
            fetched = cursor.fetchall()
            fetched  = fetched[0]
            return fetched
        except:
            print (i)
            print (fetched)

    def select_text_by_id(connection, table, i, key):
        print(i, os.getpid())
        try:
            cursor = connection.cursor(buffered=False, dictionary=True)
            cursor.execute('SELECT * FROM %s where id= %d'% (table, i))
            fetched = cursor.fetchall()
            fetched  = fetched[0]
            return fetched
        except:
            print(i)
            print (fetched)
            return ''

def json_to_csv():
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
        database, charset, table_name, out_file_path):
        db= mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset)
        csv_writer = csv.DictWriter(
                open(out_file_path, 'w'),
                 fieldnames=get_table_fields(
                    connection=db,
                    table_name=table_name)['fieldnames'],
                delimiter='\t')
        cursor = db.cursor(buffered=False, dictionary=True)
        csv_writer.writeheader()
        for i in range(1, get_table_length(db, table_name)

                           ):
                        raw = get_table_raw(cursor, table_name, i)
                        if raw:
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
        charset="utf8",
        table_name='publications',
        out_file_path='publications.csv')
