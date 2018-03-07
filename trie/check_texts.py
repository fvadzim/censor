#!censor/bin/python3

import os
from parse import LexiconCheckerAgsParser
import mysql.connector
from pathos.multiprocessing import Pool
import trie


def select_text_by_id(connectotion, table, i, key):
    print(i, os.getpid())
    try:
        cursor = connectotion.cursor(buffered=False, dictionary=True)
        cursor.execute('SELECT * FROM %s where id= %s'% (table, i))
        return cursor.fetchall()[0][key]
    except:
        return ''


def reduce_vector(trie_list=None):
    args = LexiconCheckerAgsParser().get_args_dict()
    db= mysql.connector.connect(
        host=args["host"],
        user=args["user"],
        password=args["password"],
        database=args["database"],
        charset=args["charset"])
    return (list(Pool(2).map(lambda i: trie.get_vector(
                                      select_text_by_id(
                                        db, args["table"],
                                        i, args["field"]), trie_list),
                range(1, 120))))


if __name__ == "__main__":
    pass
