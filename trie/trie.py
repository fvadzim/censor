# -*- coding:utf-8 -*-
import marisa_trie
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
import numpy as np
import os
import pymorphy2
'''
    creates and returns trie
    saves it to a file if to_be_saved is True
    dictionary example:
        abc
        abcd
        abcd
        ...
        zzz
'''


def create_trie(dictionary_path,
                to_be_saved=True,
                save_as=None):
    dictionary_words = []
    with open(dictionary_path, 'r') as f:
        for line in f:
            dictionary_words.append(line.rstrip().lower())
    trie = marisa_trie.Trie(dictionary_words)
    if to_be_saved:
        if not save_as:
            save_as = os.path.split(dictionary_path)[-1].split('.')[0]+'.marisa'
        trie.save(save_as)
    return trie


'''
    load trie of ".marisa" format.
    if file exists returns trie
    raises OSError else
'''


def load_trie(trie_path):
    if not (os.path.exists(os.path.abspath(trie_path))
            or os.path.exists(os.path.join(os.getcwd(), trie_path))):
        print("##################################")
        print(os.path.abspath(trie_path))
        print(trie_path)
        print("##################################")
        raise OSError('''error while loading trie {}.
                             Check if the file exists.
                             Check if file access mode not less 400'''.format(trie_path))
    trie = marisa_trie.Trie()
    trie.load(os.path.abspath(os.path.join(os.getcwd(), trie_path)))
    return trie


'''
    Check text on occuruncies from trie in "*.marisa" format
    (marisa_trie librarian format).
    stemmer and ru_stemmer are stemmers from nltk.stem
    pymorphy.morph - stemmer from pymorphy(for russian lang)
'''


def get_trie_list(trie_pathes):
    trie_list = []
    for trie_path in trie_pathes:
        trie_list.append(load_trie(trie_path))
    return trie_list


def get_occurancies(text, trie):

    stemmer = SnowballStemmer('russian')
    morph = pymorphy2.MorphAnalyzer()
    tokens = ([morph.parse(word)[0].normal_form for word in word_tokenize(text)]
              + [stemmer.stem(word) for word in word_tokenize(text)])
    ans = []
    for token in tokens:
        if token in trie:
            ans.append(token)
    return ans


'''
    returns bool vector of was/was not a particluar lexicon in text
    trie_pathes: list of pathes to trie
'''


def get_vector(text, trie_list):
    v = np.zeros(len(trie_list))
    for index, trie in enumerate(trie_list):
        if len(get_occurancies(text,  trie)):
            v[index] = 1
    return v


if __name__ == "__main__":
    pass
