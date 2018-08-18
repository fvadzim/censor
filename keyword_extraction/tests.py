import unittest
import os
from ..text_representations.text import Text
from ..keyword_extraction.keyword import *


class TestTextReprCase(unittest.TestCase):

    def test_get_extractor(self):
        self.assertIsInstance(get_extractor('tr'), KeyWordsExtractor)
        self.assertIsInstance(get_extractor('ti'), KeyWordsExtractor)
        self.assertIsInstance(get_extractor('r'), KeyWordsExtractor)

    def test_get_tfidf(self):
        text = ''
        with open(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'test_data/text_1.txt')) as test_text:
            text = ''.join(test_text.readlines())
        tf_idf = get_extractor('ti')
        tf_idf.update_idf(BagOfWords(text))
        self.assertLessEqual(len(get_extractor('r').get_key_words(text)), len(text.split()))
        self.assertLessEqual(len(tf_idf.get_key_words(text)), len(text.split()))
        self.assertLessEqual(len(get_extractor('tr').get_key_words(text)), len(text.split()))

if __name__ == '__main__':
    unittest.main()