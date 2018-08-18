import unittest
import os
from ..keyword_extraction.keyword import get_extractor, Rake, TfIdf, TextRank
from ..text_representations.bag_of_words import BagOfWords, Text

class TestNew(unittest.TestCase):

    def assertIsExtractor(self, rake, text):
        self.assertIsInstance(rake.get_key_words(text), list)
        self.assertIsInstance(rake.get_key_words(text)[0], tuple)
        self.assertIsInstance(rake.get_key_words(text)[0][0], str)
        self.assertIsInstance(rake.get_key_words(text)[0][1], float)

    def test_proper_extractor(self):
        rake = get_extractor('r')
        self.assertIsInstance(rake, Rake)
        tf_idf = get_extractor('ti')
        self.assertIsInstance(tf_idf, TfIdf)
        text_rank = get_extractor('tr')
        self.assertIsInstance(text_rank, TextRank)

    def test_rake(self):
        rake = get_extractor('r')
        with open(os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'test_data/text_1.txt')) as txt_file:
            text = ''.join(txt_file.readlines())
        self.assertIsExtractor(rake, text)

    def test_tf_idf(self):
        ti = get_extractor('ti')
        with open(os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'test_data/text_1.txt')) as txt_file:
            text = ''.join(txt_file.readlines())
        ti.update_idf(BagOfWords(text, 'en'))
        self.assertIsExtractor(ti, text)

    def test_text_rank(self):
        tr = get_extractor('tr')
        with open(os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'test_data/text_1.txt')) as txt_file:
            text = ''.join(txt_file.readlines())

        self.assertIsExtractor(tr, text)


if __name__ == '__main__':
    unittest.main()