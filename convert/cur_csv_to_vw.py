# -*- coding:utf-8 -*-
import os, sys
cur_file_path = os.path.abspath(__file__)
print("cur file path: ", cur_file_path)
sys.path.append(cur_file_path)
sys.path.append(os.path.dirname(cur_file_path))
sys.path.append(os.path.dirname(os.path.dirname(cur_file_path)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(cur_file_path))))

print(sys.path)
import multiprocessing
import json
import os
import argparse
import csv
import functools
from  censor.convert.text_process import *
from  censor.trie import trie

csv.field_size_limit(500 * 1024 * 1024)
locker = multiprocessing.Lock()

'''
    Module main goal is to get folowwing format from dict representation.
    *Following format* is https://github.com/JohnLangford/vowpal_wabbit/wiki/Input-format.
'''


class VwReader:
    def __init__(self, file_, splitter, id_at_beginning=True):
        self.__file = file_
        self.__splitter = splitter
        self.__id_at_beginning = id_at_beginning

    def __iter__(self):
        return self.next()

    def next(self):
        for line in self.__file:
            dict_ = dict()
            for modality in line.split(self.__splitter)[bool(self.__id_at_beginning):]:
                #         print(line.split(splitter)[bool(id_at_beginnning):][0])
                modality_name, *tokens = modality.strip().split(' ')
                dict_[modality_name] = dict()
                #         print(modality_name, tokens)
                for token in tokens:
                    token_name, *token_freq = token.split(':')
                    if token_freq:
                        dict_[modality_name][token_name] = int(token_freq[0])
                    else:
                        dict_[modality_name][token_name] = 1
            #         print(dict_[modality_name].items())
            yield dict_


def get_texts_from_json_files(path_to_folder):
    """

    :param path_to_folder: unix path to json file
    :return list for readed json files
    """
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


def write_dict_row_to_vw_file_atomic(row, vw_path, **kwargs):
    with locker:
        with open(vw_path, "a") as vw_file:
            vw_file.write(post_to_corpus_line(row, **kwargs))


def write_in_parallel_to_vw(vw_file, dict_rows):
    '''
    use parallel(but not very fast) writing to vowpal wabbit file
    :param vw_file:
    :param dict_rows:
    :return:
    '''
    write_dict_row_to_vw_file_default = functools.partial(
        write_dict_row_to_vw_file_atomic, vw_path=vw_file)
    p = multiprocessing.Pool(10)
    return p.map(write_dict_row_to_vw_file_default, dict_rows)


def get_vw_rows_from_csv_rows(dict_rows):
    p = multiprocessing.Pool(10)
    return p.map(post_to_corpus_line, dict_rows)


def get_csv_rows_materialized(reader_csv):
    return [row for row in reader_csv]


def delete_stop_words_from_wv_file(file_path):
    '''
    It is not good idea to use this funciton. Try to provide your text with proper filtering before creating vw file.
    Hovewer it is cheaper to fix than to create new one.
    :param file_path:
    :return:
    '''
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
    """
    creates csv readed which reads only specified fields.
    :param fieldnames: names of fields to read.
    :rtype: object
    """
    return csv.DictReader(
        input_file,
        fieldnames=fieldnames,
        delimiter=delimiter
    )


def get_headers(input_file, delimiter='\t'):
    '''

    :param input_file: path to input fie
    :param delimiter: delimet of csv file
    :return: list of headers of input file
    '''
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
    parser.add_argument("--lang", help="path to output file")
    parser.add_argument("--fields", nargs='+',  help="list of fields to sue")
    args = parser.parse_args()
    print("/ARGS : ", args)
    with open(args.input_file, 'r') as input_file:
        headers = get_headers(input_file, '\t')
        csv_reader = get_dict_reader(input_file, headers, '\t')
        dict_rows = get_csv_rows_materialized(csv_reader)
        pool = multiprocessing.Pool(10)
        for row in dict_rows:
            pool.apply_async(
                write_dict_row_to_vw_file_atomic,
                args=(row, args.output_file),
                kwds=dict(lang=args.lang, fields=args.fields, category_name='category_id'))
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()