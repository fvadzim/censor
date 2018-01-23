# -*- coding:utf-8 -*-
import csv
import os
import sys
import argparse
import multiprocessing
import functools
go = os.path.abspath(os.path.dirname(__file__))
away =  os.path.dirname(go)

sys.path.append(go)
sys.path.append(away)

print(sys.path)

from collections import Counter
from  filter.filter import Filter
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.getcwd()))
csv.field_size_limit(500 * 1024 * 1024)
from trie import trie




locker = multiprocessing.Lock()

def construct_bow_with_filtering(words):
            return [(
                word.replace(' ', '_').replace(':', '_').replace('|', '_').replace('\t', '_') +
                ('' if cnt == 1 else ':%g' % cnt)) for word, cnt in words.items()]

def construct_bow(words):
    return [(word +('' if cnt == 1 else ':%g' % cnt)) for word, cnt in words.items()]

def words_count(text):
    #print(text[:10])
    return Counter(Filter().get_tokens(text))

def get_texts_from_json_files(path_to_folder):
    json_list = (json.loads(abs_file_name)

            for abs_file_name in

            [os.path,join(path_to_folder, file_name)
                     for file_name in os.path.listdir(path_to_folder)])
    pool = multiprocessing.Pool(20)
    pool.map(write_json_row_to_vw_file ,json_list)
    pool.close()
    pool.join()

def write_json_row_to_vw_file(row, vw_path):
    with locker:
         with open(vw_path, "a") as vw_file:
            vw_file.write(post_to_corpus_line(row))

def post_to_corpus_line(row, fields=('content', 'title') , category=True):
    parts = [row['id']]+[('|@' +
                          field +
                          ('', ' ')[bool(
                              len(construct_bow(words_count(row[field]))))] +
                          ' '.join(construct_bow(words_count(row[field]))))
                         for field in fields]
    #print(parts)
    if category:
        parts.append("|@category_id " + row["category_id"])
    return ' '.join(parts)+'\n'


def write_dict_row_to_vw_file(row, vw_path):
    with locker:
         with open(vw_path, "a") as vw_file:
            vw_file.write(post_to_corpus_line(row))


def write_parallely_to_vw(vw_file, dict_rows):
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
        refactored_line = ''
        for line in wv_file:
            refactored_line = [word for word in line.split()
                if not word.split(":")[0] in stop_words_trie]
            print(len(refactored_line), " : ", len(line.split()))
            refactored_line.append("\n")
            lines.append(" ".join(refactored_line))
    with open(file_path, "w") as wv_file:
        wv_file.writelines(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert CSV file to Vowpal Wabbit format.')
    parser.add_argument("input_file",  help="path to csv input file")
    parser.add_argument("output_file", help="path to output file")
    args = parser.parse_args()
    #delete_stop_words_from_wv_file(args.output_file)
    print(trie.load_trie("stopwords.marisa").keys())
    '''with open(args.input_file, 'r') as input_file:
        headers = input_file.readline().strip().split('\t')
        print(headers)
        csv_reader = csv.DictReader(input_file,
                                    fieldnames=headers,
                                    delimiter='\t')
        dict_rows = get_csv_rows(csv_reader)

        print(len(dict_rows))
    pool = multiprocessing.Pool(10)
    for row in dict_rows:
        pool.apply_async(write_dict_row_to_vw_file, args=(row, args.output_file))
    pool.close()
    pool.join()
        #write_parallely_to_vw(args.output_file, dict_rows)
        #open(args.output_file, 'w').writelines(
        #    get_vw_rows_from_scv_rows(list(dict_rows)))'''
