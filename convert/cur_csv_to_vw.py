# -*- coding:utf-8 -*-
import csv
import os
import sys
import argparse
import multiprocessing
from collections import Counter
from filter.filter import Filter
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.getcwd()))
csv.field_size_limit(500 * 1024 * 1024)


def construct_bow(words):
            return [(
                word.replace(' ', '_').replace(':', '_').replace('|', '_').replace('\t', '_') +
                ('' if cnt == 1 else ':%g' % cnt)) for word, cnt in words.items()]


def words_count(text):
    return Counter(Filter().get_tokens(text))


def post_to_corpus_line(row, fields=('content', 'title', 'category_id',)):
    parts = [row['id']]+[('|@' +
                          field +
                          ('', ' ')[bool(
                              len(construct_bow(words_count(row[field]))))] +
                          ' '.join(construct_bow(words_count(row[field]))))
                         for field in fields]
    return ' '.join(parts)+'\n'


def get_vw_rows_from_scv_rows(dikt_rows):
    p = multiprocessing.Pool(10)
    return p.map(post_to_corpus_line, dikt_rows)


def get_csv_rows(reader_csv):
    return [row for row in reader_csv]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert CSV file to Vowpal Wabbit format.')
    parser.add_argument("input_file",  help="path to csv input file")
    parser.add_argument("output_file", help="path to output file")
    args = parser.parse_args()
    with open(args.input_file, 'r') as input_file:
        headers = input_file.readline().strip().split('\t')
        print(headers)
        csv_reader = csv.DictReader(input_file,
                                    fieldnames=headers,
                                    delimiter='\t')
        dict_rows = get_csv_rows(csv_reader)
        print(len(dict_rows))
        open(args.output_file, 'w').writelines(
            get_vw_rows_from_scv_rows(list(dict_rows))
        )
