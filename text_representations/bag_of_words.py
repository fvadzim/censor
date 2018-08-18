from ..convert.text_process import words_count_filtered, Text


class BagOfWords:
    def __init__(self, text, language='en'):
        self.word_counter = words_count_filtered(Text(text, language))
        self.overall_cnt = sum(self.word_counter.values())

    @staticmethod
    def from_counter(word_counter):
        bag_of_words = BagOfWords('')
        bag_of_words.word_counter = word_counter
        bag_of_words.overall_cnt = sum(bag_of_words.word_counter.values())
        return bag_of_words

    def words(self):
        for word in self.word_counter:
            yield word

    def get_frequency(self, word):
        return self.word_counter[word]

    def get_overall_cnt(self):
        return self.overall_cnt

    def get_counter(self):
        return self.word_counter

    def __str__(self):
        return str(list(self.word_counter.items()))

