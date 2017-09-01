# -*- coding:utf-8 -*-
import json
import csv
import os
# import vowpalwabbit
# import mysql.connector
import sys
import nltk
# from nltk.stem.snowball import SnowballStemmer
# from nltk import word_tokenize
import numpy as np
# import os
import pymorphy2 
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
#from  parse import *
import datetime
import argparse
import collections
import multiprocessing
morph = pymorphy2.MorphAnalyzer()

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

    tokens = nltk.tokenize.wordpunct_tokenize(text)
    tokens = nltk.word_tokenize(text)

    for token in tokens:
        if len(token) > 2:
            token = token.lower().replace(u'ё', u'е')
            word = morph.parse(token)[0].normal_form
            if len(word) > 0:
                words[word] += 1

    return words

def post_to_corpus_line(post):
    parts = (
        # ['\'{}'.format(post["id"])] + 
        ['|content'] + construct_bow(words_count(post["content"])) +
        ['|title'] + construct_bow(words_count(post["title"])) +
        ['|category_text'] + construct_bow(words_count(post["category_text"])) 
    )
    return ' '.join(parts)

def multiprocess(output_file):
    p = multiprocessing.Pool(10)
    result = p.map(post_to_corpus_line,kek)
    output_file.write('\n'.join(result))

def oneprocess(output_file):
    for row in csv_reader:
        output_file.write(
                post_to_corpus_line(row) + '\n'
                    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description = 'Convert CSV file to Vowpal Wabbit format.' )
    parser.add_argument( "input_file",  help = "path to csv input file" )
    parser.add_argument( "output_file",  help = "path to output file" )
    args = parser.parse_args()
    with open(args.input_file) as f:
        headers = f.readline().strip().split('\t')

        f.seek(0,0)
        csv_reader = csv.DictReader(f,
                                    fieldnames=headers,
                                    delimiter='\t')
        csv_reader.__next__()

        output_file = open(args.output_file, 'w')
        
        multiprocess(output_file)