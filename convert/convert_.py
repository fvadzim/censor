import json
import csv
import os
import mysql.connector
import sys
import psycopg2
import psycopg2.extras
from interface import implements, Interface
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class ISqlRawGetter(Interface):

    def get_table_raw(self, table_name, i, cursor=None):
        raise NotImplementedError

    def get_dict_cursor(self, **kwargs):
        raise NotImplementedError

    def get_default_cursor(self, **kwargs):
        raise NotImplementedError


class SqlConnection:
    def __init__(
        self, host,
        user, password,
        database, charset=None):
        raise NotImplementedError

    def get_table_fields(self, table_name):
        self.cursor.execute("Select * FROM %s where id = 0" % (table_name,))
        return [desc[0] for desc in self.cursor.description]

    def get_table_length(self, table_name):
        cursor = self.get_default_cursor()
        cursor.execute("SELECT COUNT(*) from %s" % (table_name,));
        return cursor.fetchone()[0]

    def get_table_raw(self, table_name, i, cursor=None):
        if cursor is None:
            cursor = self.get_dict_cursor()
        cursor.execute('SELECT * FROM %s where id= %d' % (table_name, i))
        try:
            fetched = cursor.fetchone()
            return {
                key: BeautifulSoup(('', str(fetched[key]))[bool(fetched[key]) == True],
                                   "html5lib").get_text().replace(u'\xa0', u' ')
                for key in fetched.keys()}
        except:
            pass

    def get_default_cursor(self):
        return self.connection.cursor()

    def select_field_by_id(self, table_name, i, key):
        try:
            return self.get_table_raw(
                table_name=table_name, i=i)[key]
        except:
            return ''


class _MySqlConnection(SqlConnection, implements(ISqlRawGetter)):
    def __init__(self, host, user, password, database):
        super().__init__(
            host=host, user=user,
            passwor=password, database=database)
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database)
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)

    def get_dict_cursor(self):
        return self.connection.cursor(
                dictionary=True,
                buffered=False)


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

    def get_dict_cursor(self):
        return self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)


def json2csv(file_path, out_file_path):
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
        sql_converter = _MySqlConnection(
            host=host,
            user=user,
            password=password,
            database=database)
        csv_writer = csv.DictWriter(
            open(out_file_path, 'w'),
            fieldnames=sql_converter.get_table_fields(table_name),
            delimiter='\t')
        csv_writer.writeheader()
        for i in range(1, sql_converter.get_table_length(table_name)):
            raw = sql_converter.get_table_raw(table_name, i)
            if raw:
                csv_writer.writerow(raw)


if __name__=='__main__':
    pass
