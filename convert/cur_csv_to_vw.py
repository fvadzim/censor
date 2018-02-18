# -*- coding:utf-8 -*-
import csv
import os
import argparse
import multiprocessing
import functools
import json
from collections import Counter
from filter.filter import Filter
from trie import trie

csv.field_size_limit(500 * 1024 * 1024)
locker = multiprocessing.Lock()


def construct_bow_with_filtering(words):
    return [
        (word.replace(' ', '_').replace(':', '_').replace('|', '_').replace('\t', '_')
         + ('' if cnt == 1 else ':%g' % cnt)) for word, cnt in words.items()
    ]


def construct_bow(words):
    return [
        (word + ('' if cnt == 1 else ':%g' % cnt))
        for word, cnt in words.items()
    ]


def words_count(text):
    return Counter(Filter().get_all_tokens(text))


def get_texts_from_json_files(path_to_folder):
    json_list = (
        json.loads(abs_file_name) for abs_file_name in [
            os.path.join(path_to_folder, file_name) for
            file_name in os.listdir(path_to_folder)
        ]
    )
    pool = multiprocessing.Pool(20)
    pool.map(write_json_row_to_vw_file, json_list)
    pool.close()
    pool.join()


def write_json_row_to_vw_file(row, vw_path):
    with locker:
        with open(vw_path, "a") as vw_file:
            vw_file.write(post_to_corpus_line(row))


def post_to_corpus_line(
        row,
        fields=('content', 'title'),
        category=True):
    parts = [row['id']]+[('|@' +
                          field +
                          ('', ' ')[bool(
                              len(construct_bow(words_count(row[field]))))] +
                          ' '.join(construct_bow(words_count(row[field]))))
                         for field in fields]
    if category:
        parts.append("|@category_id " + row["category_id"])
    return ' '.join(parts)+'\n'


def write_dict_row_to_vw_file(row, vw_path):
    with locker:
        with open(vw_path, "a") as vw_file:
            vw_file.write(post_to_corpus_line(row))


def write_in_parallel_to_vw(vw_file, dict_rows):
    write_dict_row_to_vw_file_default = functools.partial(
        write_dict_row_to_vw_file, vw_path=vw_file)

    p = multiprocessing.Pool(10)
    return p.map(write_dict_row_to_vw_file_default, dict_rows)


def get_vw_rows_from_scv_rows(dikt_rows):
    p = multiprocessing.Pool(10)
    return p.map(post_to_corpus_line, dikt_rows)


def get_csv_rows(reader_csv):
    return [row for row in reader_csv]


def delete_stop_words_from_wv_file(file_path):
    lines = []
    stop_words_trie = trie.load_trie("stopwords.marisa")
    with open(file_path) as wv_file:
        for line in wv_file:
            refactored_line = [word for word in line.split() if not word.split(":")[0] in stop_words_trie]
            refactored_line.append("\n")
            lines.append(" ".join(refactored_line))
    with open(file_path, "w") as wv_file:
        wv_file.writelines(lines)


def get_dict_reader(input_file, fieldnames, delimiter='\t'):
    return csv.DictReader(
        input_file,
        fieldnames=fieldnames,
        delimiter=delimiter
    )


def get_headers(input_file, delimiter='\t'):
    return input_file.readline().strip().split(delimiter)


def convert_csv_column_to_json_id_set(file_path, column_name, delimiter='\t'):
    columns_values_set = dict()
    id_index = 1
    with open(file_path, "r") as csv_file:
        headers = get_headers(csv_file, delimiter)
        for row in get_dict_reader(csv_file, headers):
            if not columns_values_set.get(row[column_name], 0):
                columns_values_set[row[column_name]] = (
                    column_name + "_{0}".format(id_index,))
                id_index += 1
    return columns_values_set


def main():
    parser = argparse.ArgumentParser(description='Convert CSV file to Vowpal Wabbit format.')
    parser.add_argument("input_file",  help="path to csv input file")
    parser.add_argument("output_file", help="path to output file")
    args = parser.parse_args()
    with open(args.input_file, 'r') as input_file:
        headers = get_headers(input_file, '\t')
        csv_reader = get_dict_reader(input_file, headers, '\t')
        dict_rows = get_csv_rows(csv_reader)
        pool = multiprocessing.Pool(10)
        for row in dict_rows:
            pool.apply_async(write_dict_row_to_vw_file, args=(row, args.output_file))
    pool.close()
    pool.join()
