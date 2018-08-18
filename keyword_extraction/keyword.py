import RAKE
import textrank
import threading
import pickle
import math
from functools import wraps
import nltk
from ..text_representations.bag_of_words import BagOfWords

class KeyWordsExtractor():
    '''
    little abstract class with method to be implemented
    '''
    def get_key_words(self, text):
        raise NotImplementedError


class TfIdf(KeyWordsExtractor):
    '''
        https://en.wikipedia.org/wiki/Tf%E2%80%93idf
        Statistichal method to get keywords(most important words) from the text.
    '''
    def __init__(self, idf_dict_counter=None):
        self.lock_ = threading.Lock() #lock for each word maybe?
        if idf_dict_counter is None:
            self.idf_dict_counter = dict()
        else:
            self.idf_dict_counter = idf_dict_counter
        self.document_number = 0

    def inc_word_idf(self, word):
            with self.lock_:
                self.idf_dict_counter[word] = self.idf_dict_counter.get(word, 0) + 1

    def update_idf(self, bag_of_words):
            with self.lock_:
                for word in bag_of_words.words(): #iterat
                        self.idf_dict_counter[word] = self.idf_dict_counter.get(word, 0) + 1
                self.document_number += 1

    def get_tf(self, word, bag_of_words):
        return bag_of_words.get_frequency(word) / bag_of_words.get_overall_cnt()

    def get_idf(self, word):
        return math.log(self.document_number / (1 + self.idf_dict_counter[word]))

    def get_tfidf(self, word, bag_of_words, update=True):
        if update:
            self.update_idf(bag_of_words)
        return self.get_tf(word, bag_of_words) * self.get_idf(word)

    def get_key_words(self, text):
        bag_of_words = BagOfWords(text)
        return sorted([
                        (word,
                        self.get_tfidf(word, bag_of_words, False)) for word in bag_of_words.words() if word in self.idf_dict_counter],
            key=lambda x :x[1],
            reverse=True
        )


class TextRank(KeyWordsExtractor):
    '''
        https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf
    '''
    def get_key_words(self, text):
        key_phrases = textrank.extract_key_phrases(text)
        return list(zip(key_phrases, [1.] * len(key_phrases)))


class Rake(KeyWordsExtractor):
    '''
    https://www.researchgate.net/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents
    '''
    def __init__(self, lang):
        self.rake_ = RAKE.Rake(nltk.corpus.stopwords.words('english'))

    def get_key_words(self, text):
        return sorted(self.rake_.run(text), key=lambda x: x[1], reverse=True)


def get_extractor(algo):
    """
    :param algo:
    :return: extractor based on algorithm, specified by parametr,
    algo parametr must be 'r' for 'Rake' algorithm or 'ti' for 'TF_IDF algorithm or 'tr' for TextRank
    """
    if 'r' == algo:
        return Rake()

    if 'ti' == algo:
        return TfIdf()

    if 'tr' == algo:
        return TextRank()
    raise ValueError("algo parametr must be 'r' for 'Rake' algorithm or 'ti' for 'TF_IDF algorithm or 'tr' for TextRank ")



