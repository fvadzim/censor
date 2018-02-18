#!censor/bin/python3
import os
import csv
import trie as Trie
import numpy as np
from parse import LexiconCheckerAgsParser
import mysql.connector
from pathos.multiprocessing import Pool


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
                range(1,120))))


if __name__ == "__main__":
    csv_reader = csv.DictReader(
            open("contents.csv", 'r'),
             fieldnames =  ['id',
             'title',	'category_id',	'excerpt',
             'content',	'slug',	'created_at',	'updated_at',	'photo',
             'keywords',	'published',
             'author_id',	'views',	'published_at',	'mongo_id',	'type',	'repost_count',
             'is_old',	'advertisement_type',	'blocked',	'special_project_id',
             'branding_id',	'poll_id',	'publication_datetime',	'activity_time_trackingold_category_id',
             'banner_id',	'is_rfrm',	'rfrm_id',	'rfrm_url'],
            delimiter='\t')
    print(os.path.exists('trie/obscene_lexicon.marisa'))
    tries = [Trie.load_trie( 'trie/gambling.marisa'),
            Trie.load_trie('trie/alco.marisa'),
            Trie.load_trie('trie/obscene_lexicon.marisa')]
    res, cnt = np.zeros( 3), 0

    for row in csv_reader:
        if cnt < 3940:
            text = row['content']
            for j, trie in enumerate(tries):
                if (len(Trie.get_occurancies(text, trie))):
                    res[ j] += 1
        print(res, cnt)
        cnt += 1
    print( np.add.reduce(res, 0)/3940 )
