# -*- coding:utf-8 -*-
import nltk
from collections import Counter
from ..filter.filter import get_filter
from ..filter.filter import Filter
from ..text_representations.text import Text


def construct_bow(words_cnt_dict):
    """
    :param words_cnt_dict: must be an an associative array (key-value dict)[dict, collections.Counter and etc.]
    :return: list of strings.
    Examples:
        >>> print(construct_bow(dict(first_token=1, second_token=2)))
        ["first_token", "second_token:2"]
    """
    if not isinstance(words_cnt_dict, dict):
        raise ValueError("word_cnt_dict must be assotiative array(dict of inherited from)")
    return [
        (word + ('' if cnt == 1 else ':%g' % cnt))
        for word, cnt in words_cnt_dict.items()
    ]


def construct_bow_with_filtering(word_cnt_mapping):
    """
    :param word_cnt_mapping: must be an an associative array (key-value dict)[dict, collections.Counter and etc.]
    :return: list of strings.
    """
    if not isinstance(word_cnt_mapping, dict):
        raise ValueError("word_cnt_mapping must be assotiative array(dict of inherited from)")
    return [
        (word.replace(' ', '_').replace(':', '_').replace('|', '_').replace('\t', '_')
         + ('' if cnt == 1 else ':%g' % cnt)) for word, cnt in word_cnt_mapping.items()
    ]


def words_count_filtered(text, text_filter=None):
    """
    :param text: text_representation.Text
    :param text_filter: Filter
    :return: Counter(key: token, value: frequency in text)
    """
    if not isinstance(text, Text):
        raise ValueError("text must be of type Text[watch text_represenations module]")

    if text_filter is not None:
        if not isinstance(text_filter, Filter):
            raise ValueError("text must be of type Text[watch text_represenations module]")
        return Counter(text_filter.get_tokens(text.get_text()))
    return Counter(get_filter(text.get_language()).get_tokens(text.get_text()))


def words_count(text, text_filter=None):
    """
    :param text: text_representation.Text
    :param text_filter: Filter
    :return: Counter(key: token, value: frequency in text)
    """
    if not isinstance(text, Text):
        raise ValueError("text must be of type Text[watch text_represenations module]")
    if filter is not None:
        return Counter(text_filter.get_all_tokens(text.get_text()))
    return Counter(get_filter(text.get_language().get_all_tokens(text.get_text())))


def construct_vw_modality(modality_name, modality_text, filtering=False):
    """
    :param modality_name: str
    :param modality_text: str
    :param filtering: bool
    :return: str

    Examples:
        >>> print(construct_vw_modality(dict("content", "token3 token2 token3 token4. token1 token1 token2")))
        "|@content token1:1 token2:2 token3:2 token4:1"

    """
    words_counter = (words_count, words_count_filtered,)[int(filtering)]
    bow = construct_bow(words_counter(modality_text))
    return '|@' + modality_name + ('', ' ')[bool(len(bow))] + ' '.join(bow)


def post_to_corpus_line(
        row,
        fields=('content', 'title'),
        id_name='id',
        category_name=None,
        filtering=True,
        lang='en'
):
    parts = [row[id_name]]+[construct_vw_modality(field, Text(row[field], language=lang), filtering=filtering) for field in fields]
    print(row[id_name])
    if category_name:
        parts.append("|@{} {}".format(category_name, row[category_name]))
    return ' '.join(parts)+'\n'


def get_bigrams(text):
    """
    :param text: Text
    :return: generator for token pairs of input text
    """
    filter_ = get_filter(text.get_language())
    return nltk.bigrams(filter_.get_tokens(text.get_text()))


if __name__ == "__main__":
    pass