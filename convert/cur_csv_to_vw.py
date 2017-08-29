# -*- coding:utf-8 -*-
import json
import csv
import os
import vowpalwabbit
import mysql.connector
import sys
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
import numpy as np
import os
import pymorphy2
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
#from  parse import *
import datetime
import argparse
from collections import Counter
def get_kokens(text):

    morph = pymorphy2.MorphAnalyzer()
    return [morph.parse(word.lower())[0].normal_form for word in word_tokenize(text) if ((not ':' in word) and (not len(word)==1 or word== 'i')
                                                                                        and not word[0] in [str(i) for i in range(10)])]


def construct_line(id_num, cnt_tokens):
    return id_num + ' |@text '+' '.join([ key+':'+str(cnt_tokens[key]) for key in cnt_tokens.keys() ] )+'\n'



if __name__ =="__main__":
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
        i =0
        for row in csv_reader:
            i+=1
            if i==1001:
                break
            output_file.write(
                    construct_line(
                        row['id'],
                        Counter(get_kokens(row['content'])))
                        )
