import unittest
import os
from ..text_representations.bag_of_words import BagOfWords
from ..convert.text_process import *

class TestNew(unittest.TestCase):

    def test_get_lang(self):
        self.assertEqual(Text("hey you", 'en').get_language(), 'en')

    def test_bigrams(self):
        bigrams = get_bigrams(Text("Я увидел кошку.", 'ru'))
        print(list(bigrams))
        self.assertIsInstance(list(bigrams), list)

    def test_construct_bow(self):
        with open(os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'test_data/text_1.txt')) as txt_file:
            text = ''.join(txt_file.readlines())
        bag_of_words = BagOfWords(text, 'en')
        self.assertIsInstance(construct_bow(bag_of_words.get_counter()), list)
        self.assertIsInstance(construct_bow_with_filtering(bag_of_words.get_counter()), list)

    def test_word_count(self):
        with open(os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'test_data/text_1.txt')) as txt_file:
            text = ''.join(txt_file.readlines())
        bag_of_words = BagOfWords(text, 'en')
        self.assertIsInstance(construct_bow(bag_of_words.get_counter()), list)
        self.assertIsInstance(construct_bow_with_filtering(bag_of_words.get_counter()), list)

if __name__ == '__main__':
    unittest.main()
