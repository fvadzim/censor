# cur_file_path = os.path.abspath(__file__)
# from scipy.spatial.distance import cosine
# sys.path.append(cur_file_path)
# sys.path.append(os.path.dirname(cur_file_path))
# sys.path.append(os.path.dirname(os.path.dirname(cur_file_path)))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(cur_file_path))))
import  string
import nltk
from pymystem3 import Mystem
# from trie import trie
from marisa_trie import Trie
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


filtered_parts = {
    "PART", "APRO", "PR", "SPRO",
    "ANUM", "ADVPRO", "CONJ"
}


class EnglishStemmer:
    '''
        class for english text normalization.
        Steps:
        1. https://en.wikipedia.org/wiki/Lexical_analysis#Tokenization
        2. https://en.wikipedia.org/wiki/Lemmatisation
        3. https://en.wikipedia.org/wiki/Stemming
        widely use https://www.nltk.org/ library
    '''
    def __init__(self):

        self.tokenizer__ = nltk.tokenize.RegexpTokenizer(r'\w+')
        self.lemmatizer__ = WordNetLemmatizer()
        self.stemmer__ = nltk.stem.SnowballStemmer("english", ignore_stopwords=False)

    @staticmethod
    def get_wordnet_pos(treebank_tag):
        """
        :param treebank_tag: one-symbol str representing tag
        :return: tag in wordnet context
        """
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def get_rid_of_punctuation(self, sentence):
        return self.tokenizer__.tokenize(sentence)

    def lemmatize(self, token, pos='n'):
        return self.lemmatizer__.lemmatize(token, pos)

    def stem(self, word):
        return self.stemmer__.stem(word)


class Filter:
    '''
        Abstract class to implement filtering text from stopwords and punctuation and also normalize all the tokens.
    '''
    def __init__(self, path_to_stop_words_trie=None):
        """

        :param path_to_stop_words_trie: path to file with all the stopwords.
        see https://github.com/pytries/marisa-trie/blob/master/docs/tutorial.rst
        """
        if path_to_stop_words_trie:
            self.stop_words_trie = Trie()
            self.stop_words_trie.load(path_to_stop_words_trie)
        self.punctuation = set(string.punctuation + string.whitespace + string.digits + '\n')

    def get_tokens(self, text):
        '''
        :param text: str
        :return: list of tokens without getting rid of stopwords.
        '''
        raise NotImplementedError("should implement this")

    def get_all_tokens(self, text):
        '''
        :param text: str
        :return: list of tokens with getting rid of stopwords.
        '''
        raise NotImplementedError("should implement this")


class FilterEnglish(Filter):

    def __init__(self, path_to_stop_words_trie=None):
        super().__init__(path_to_stop_words_trie)
        self.lexer__ = EnglishStemmer()
        if not path_to_stop_words_trie:
            self.stop_words_trie = Trie(stopwords.words("english"))

    def get_tokens(self, text):
        from nltk.tokenize import sent_tokenize
        tokens = [word for sent in sent_tokenize(text) for word in
                  self.lexer__.get_rid_of_punctuation(sent) if word not in self.stop_words_trie]
        return [word.lower() for word, pos_tag in nltk.pos_tag(tokens)]

    def get_all_tokens(self, text):
        return [
            self.lexer__.lemmatize(
                word, pos=self.lexer__.get_wordnet_pos(speech_part)).lower()
            for word, speech_part in self.get_tokens(text) if word not in self.stop_words_trie]


class FilterRussian(Filter):

    def __init__(self, path_to_stop_words_trie=None):
        super().__init__(path_to_stop_words_trie)
        self.stemmer_ = Mystem()
        if not path_to_stop_words_trie:
            self.trie = Trie(stopwords.words("russian"))
        print("self.punkt : ", self.punctuation)

    def get_tokens(self, text):
        return [lex for lex in
                [self.get_word_from_token(word)
                 for word in self.stemmer_.analyze(text)] if (lex is not None and lex not in self.trie)]

    def get_all_tokens(self, text):
        tokens = []
        for token_info in self.stemmer_.analyze(text):
            if 'analysis' in token_info:
                if len(token_info['analysis']):
                    if 'lex' in token_info['analysis'][0]:
                        tokens.append(token_info["analysis"][0]["lex"])
        return tokens

    @staticmethod
    def get_word_from_token(token):
        if "analysis" not in token:  # to be changed!
            return None
        if not token["analysis"]:  # to be changed!
            return None
        if "сравн" in token:
            return None
        if "gr" not in token["analysis"][0]:  # to be changed!
            return None

        if any(token["analysis"][0]["gr"].startswith(grammer) for grammer in filtered_parts):
            return None

        if 'фам,жен' in token["analysis"][0]["gr"]:
            return "фамиия_жен"

        if 'имя,жен' in token["analysis"][0]["gr"]:
            return "имя_жен"

        if 'фам,муж' in token["analysis"][0]["gr"]:
            return "фамиия_муж"

        if 'имя,муж' in token["analysis"][0]["gr"]:
            return "имя_муж"

        if 'фам,муж' in token["analysis"][0]["gr"]:
            return "имя_муж"

        return token["analysis"][0]["lex"]


def get_filter(language=None, path_to_stop_words_trie=None):
    """
    :param language: str representing language to get filter for
    :param path_to_stop_words_trie: unix path
    :return: Filter
    """
    if language.lower() not in ('en', "ru", "english", "russian"):
        raise BaseException("Language must be 'en' or 'ru' ")
    if language.lower() in ("ru", "russian"):
        return FilterRussian(path_to_stop_words_trie)
    else:
        return FilterEnglish(path_to_stop_words_trie)


if __name__ == "__main__":
    text_example = '''
    Björk Guðmundsdóttir (Icelandic pronunciation: [ˈpjœr̥k ˈkvʏðmʏntsˌtouhtɪr], born 21 November 1965),[2] 
    known as Björk (/bjɜːrk/),[3] is an Icelandic singer, songwriter, actress, record producer, and DJ.
    Over her four-decade career, she has developed an eclectic musical style that draws on a wide range of 
    influences and genres spanning electronic, pop, experimental, classical, trip hop, IDM, 
    and avant-garde styles. She initially became known as the lead singer of the alternative rock band The Sugarcubes
    , whose 1987 single "Birthday" was a hit on US and UK indie stations and a favorite among music critics
    .[4] Björk embarked on a solo career in 1993, coming to prominence as a solo artist with albums such as 
    Debut (1993), Post (1995), and Homogenic (1997), while collaborating with a range of artists and exploring a variety
    of multimedia projects.
    Björk has won five BRIT Awards, four MTV Video Music Awards, one MOJO Award, three UK Music Video Awards, 21 
    Icelandic Music Awards and, in 2010, the Polar Music Prize from the Royal Swedish Academy of Music in recognition 
    of her "deeply personal music and lyrics, her precise arrangements and her unique voice."[12][13] She has also been 
    nominated for 14
    Grammy Awards, one Academy Award, and two Golden Globe Awards. In 2015, Björk was included in Time Magazine's list 
    of the 100 most influential people in the world.[14][15] She won the Best Actress Award at the 2000 Cannes Film 
    Festival for her performance in the film Dancer in the Dark.[16] A full-scale retrospective exhibition dedicated to 
    Björk was held at the Museum of Modern Art in 2015.[17]
    I have forgotten somebody's kek.
    '''
    print("text example : \n", text_example)
    filter_english = FilterEnglish()
    print("tokens : \n", filter_english.get_all_tokens(text_example))
