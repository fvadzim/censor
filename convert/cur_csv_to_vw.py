# -*- coding:utf-8 -*-
import json
import csv
import os
import sys
import nltk
import numpy as np
import pymorphy2
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.getcwd()))
import datetime
import argparse
import collections
import multiprocessing
import functools
csv.field_size_limit(500 * 1024 * 1024)
import codecs
import goslate
from translator import Translator
def construct_bow(words, translate=''):

            return [
            (
                word.replace(' ', '_').replace(':', '_').replace('|', '_').replace('\t', '_') +
                ('' if cnt == 1 else ':%g' % cnt)
            )
            for word, cnt in words.items()]


def words_count(text):
    words = collections.Counter()
    space_chars = u',?!-«»“”’*…/_.\\'
    for c in space_chars:
        text = text.replace(c, ' ')
    morph = pymorphy2.MorphAnalyzer()
    tokens = nltk.tokenize.wordpunct_tokenize(text)
    tokens = nltk.word_tokenize(text)
    for token in tokens:
        if len(token) > 2 or token.isdigit():
            token = token.lower().replace(u'ё', u'е')
            word = morph.parse(token)[0].normal_form
            if len(word):
                words[word] += 1
    return words

def post_to_corpus_line(row,
                        fields=[
                            'content',
                            'title',
                            'category_id'],
                        translator=Translator('be','ru')
                        ):
    # print('title', construct_bow(words_count(row['title'])))
    # print('content', construct_bow(words_count(row['content'])))
    parts = [row['id']]+[('|@'
                        + field
                        +('', ' ')[bool(len(construct_bow(words_count(row[field]))))]
                        + ' '.join(construct_bow(words_count(translator.translate(row[field])))))
        for field in fields]


#
    # print(parts)
    return ' '.join(parts)+'\n'


def get_vw_rows_from_scv_rows(dict_rows):
    p = multiprocessing.Pool(10)
    return p.map(post_to_corpus_line, dict_rows)



def get_csv_rows(csv_reader):
    return [row for row in csv_reader]


class kek():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description = 'Convert CSV file to Vowpal Wabbit format.' )
    parser.add_argument( "input_file",
                        help = "path to csv input file" )
    parser.add_argument( "output_file",
                        help = "path to output file" )

    # parser.add_argument()
    args = parser.parse_args()
    with open(args.input_file, 'r') as input_file:
        headers = input_file.readline().strip().split('\t')
        print(headers)
        # f.seek(0,0)
        csv_reader = csv.DictReader(input_file,
                                    fieldnames=headers,
                                    delimiter='\t')
        dict_rows = get_csv_rows(csv_reader)
        print(len(dict_rows))
        open(args.output_file,'w').writelines(
            get_vw_rows_from_scv_rows(list(dict_rows))
        )
