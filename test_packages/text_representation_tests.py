import unittest
import os
from ..text_representations.text import Text
from ..text_representations.bag_of_words import BagOfWords


class TestTextReprCase(unittest.TestCase):

    def test_get_lang(self):
        self.assertEqual(Text("hey you", 'en').get_language(), 'en')

    def test_bag_of_words(self):
        with open(os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'test_data/text_1.txt')) as txt_file:
            text = ''.join(txt_file.readlines())
        bag_of_words = BagOfWords(text, 'en')
        self.assertIsInstance(bag_of_words.word_counter, dict)


if __name__ == '__main__':
    unittest.main()
