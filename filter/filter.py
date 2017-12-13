import functools

from pymystem3 import Mystem


class Filter():
    def __init__(self, path_to_stop_words_trie=None):
        self.stemmer_ = Mystem()
        # if path_to_stop_words_trie:
        #    self.stop_words_trie = trie.load_trie(path_to_stop_words_trie)
        # else:
        #    self.trie = trie.marisa_trie([])

    filtered_parts = {
        "PART", "APRO", "PR" 
        "SPRO", "ANUM", "ADVPRO", "CONJ"} 
    

    
    def get_word_from_token(self, token):
        print(token)

        if not "analysis" in token:  # to be changed!
            return None
        
        if not token["analysis"]:  # to be changed!
            return None

        if "сравн" in token:
            return None

            

        if not "gr" in token["analysis"][0]:  # to be changed!
            return None

        if token["analysis"][0]["gr"].startswith(filtered_parts):
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

    def get_tokens(self, text):
        return [lex for lex in
                [self.get_word_from_token(word) for word in self.stemmer_.analyze(text)] if None != lex]

