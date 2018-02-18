from yandex import Translater as YandexTranslator
api_key = 'trnsl.1.1.20170930T213403Z.13a44ae7d6a9727a.8c2d023adb08bcb22ad55cbb593ec110e098399e'


class Translator:
    def __init__(self, lang_from='be', lang_to='ru'):
        self._translator = YandexTranslator()
        self._translator.set_key(api_key)
        self._translator.set_from_lang(lang_from)
        self._translator.set_to_lang(lang_to)

    def translate(self, text):
        self._translator.set_text(text)
        return self._translator.translate()

    def detect_lang(self, text):
        self._translator.set_text(text)
        return self._translator.detect_lang()


if __name__ == "__main__":
    translator = Translator()
    word = "Палёт над гняздом зязюліа"
    print(translator.detect_lang(word))
    print(translator.translate(word))
