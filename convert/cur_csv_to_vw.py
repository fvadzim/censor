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

def construct_bow(words):
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
        if len(token) > 2:
            token = token.lower().replace(u'ё', u'е')
            word = morph.parse(token)[0].normal_form
            if len(word) > 0:
                words[word] += 1
    return words

def post_to_corpus_line(raw,
                        fields=[
                            'content',
                            'title',
                            'category_text']
                        ):
    parts = ( functools.reduce ( lambda x, y : x + y,
    [
        [raw['id']]+
        ['|@' + field ]
        + construct_bow(words_count(raw[field]))
        for field in fields
    ]))
    return ' '.join(parts)+'\n'


def get_vw_raws_from_scv_raws(dict_raws):
    p = multiprocessing.Pool(10)
    return p.map(post_to_corpus_line, dict_raws[:1000])


def get_csv_raws(csv_reader):
    return [raw for raw in csv_reader]


class kek():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description = 'Convert CSV file to Vowpal Wabbit format.' )
    parser.add_argument( "input_file",
                        help = "path to csv input file" )
    parser.add_argument( "output_file",
                        help = "path to output file" )
    args = parser.parse_args()
    with open(args.input_file, 'r') as input_file:
        headers = input_file.readline().strip().split('\t')
        print(headers)
        # f.seek(0,0)
        csv_reader = csv.DictReader(input_file,
                                    fieldnames=headers,
                                    delimiter='\t')
        dict_raws = get_csv_raws(csv_reader)
        print(len(dict_raws))
        open(args.output_file,'w').writelines(
            get_vw_raws_from_scv_raws(list(dict_raws))
        )
