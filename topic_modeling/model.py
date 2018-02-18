import numpy as np
import copy
import pickle
from filter.filter import Filter
import artm
import pandas as pd


class Model:
    def __init__(
            self, phi_matrix, theta_matrix,
            process_number, iterations_via_document, iterations_via_collection,
            regularizators, name, background_topic_number=0, topic_names=None):
        self.__phi_matrix = phi_matrix
        if topic_names:
            self.__phi_matrix.columns = pd.core.indexes.base.Index(
                                                topic_names)
        self.__topic_matrix = self.__phi_matrix.transpose()
        self.__topic_names = tuple(self.__topic_matrix.index)
        self.__theta_matrix = theta_matrix

        self.__topic_number = phi_matrix.shape[1]  # int
        self.__process_number = process_number  # int
        self.__iterations_via_document = iterations_via_document  # int
        self.__iterations_via_collection = iterations_via_collection  # int
        self.__regulirizers = regularizators
        self.__name = name
        self.__background_topic_number = background_topic_number
        self.__default_token_distribution = pd.Series(
            np.zeros(self.__topic_number), index=self.__topic_names)

    def get_phi(self):
        return self.__phi_matrix

    def get_theta(self):
        return self.__theta_matrix

    def get_topic_number(self):
        return copy.copy(self.__topic_number)

    def get_topic_matrix(self):
        return self.__topic_matrix

    def get_topic_names(self):
        return self.__topic_names

    def get_process_number(self):
        return copy.copy(self.__process_number)

    def get_iterations_via_document(self):
        return copy.copy(self.__iterations_via_document)

    def get_iterations_via_collection(self):
        return copy.copy(self.__iterations_via_collection)

    def get_regulirizers(self):
        return copy.copy(self.__regulirizers)

    def get_name(self):
        return copy.copy(self.__name)

    def get_default_token_distribution(self):
        return self.__default_token_distribution

    def get_token_distribution(self, token, modality_num=1):
        try:
            token_distribution = self.__phi_matrix.loc[token]
            if type(token_distribution) == pd.core.frame.DataFrame:
                return token_distribution.iloc[modality_num]
            return token_distribution
        except KeyError:
            return self.__default_token_distribution

    def save(self, file_to_be_saved_in):
        with open(file_to_be_saved_in, "wb") as file_to_be_pickled_in:
            pickle.dump(self, file_to_be_pickled_in)


from scipy.spatial.distance import cosine


class TopicDestribution:
    def __init__(self, model):
        self.__filter = Filter()
        self.__model = model

    def get_distribution(self, text):
        tokens = self.__filter.get_all_tokens(text)
        if not len(tokens):
            return self.__model.get_default_token_distribution()

        result_topic_vector = sum(
            self.__model.get_token_distribution(token) for token in tokens)
        return result_topic_vector / sum(result_topic_vector)

    @staticmethod
    def get_similarity(distribution_first, distribution_second):
        return 1 - cosine(distribution_first, distribution_second)

    def get_most_similar_distribution(self, text):
        text_distribution = self.get_distribution(text)
        if tuple(text_distribution.values) == tuple(
                self.__model.get_default_token_distribution().values):
            return {}

        return text_distribution.nlargest(2).index


if __name__ == "__main__":

    topic_names_example = [
        "общая_тема_передвижение",
        "общая_тема_Беларусь",
        "общая_тема_Минск",
        "музыка",
        "фестивали",
        "тенденции в моде",
        "белорусские предлоги",
        "тенденции в it",
        "рестораны",
        "кино и искусство в РБ",
        "секс",
        "одежда",
        "туризм",
        "семья",
        "быт",
        "беларусь_государство",
        "концерт_спектакль_событие",
        "беларусь_мир",
        "архитектура",
        "фотография",
        "бизнес",
        "мировоззрение",
        "политика_литература",
        "какая-то_ерунда",
        "алкоголь",
        "интернет_порталы",
        "беларусь"
    ]
    model = artm.ARTM(num_topics=27)
    model.load(filename="devided_model_made_properly")
    my_model = Model(
        phi_matrix=model.get_phi(),
        theta_matrix="nothing",
        process_number=4,
        iterations_via_collection=10,
        iterations_via_document=10,
        regularizators={},
        name="first_of_this_class",
        background_topic_number=3,
        topic_names=topic_names_example
    )
    print((my_model.get_token_distribution("беларусь")))
    topic_destribution = TopicDestribution(my_model)

    print(topic_destribution.get_most_similar_distribution(
        '''На настоящий момент Бьорк разработала свой собственный эклектичный 
        музыкальный стиль, который включает в себя аспекты электроники, классики, 
        авангардной музыки, альтернативной танцевальной музыки, рока и джаза. Бьорк 
        написала музыку к фильму «Танцующая в темноте» Ларса фон Триера, в котором 
        сыграла главную роль и получила приз как лучшая актриса на Каннском кинофестивале. 
        Также она приняла участие в качестве композитора и актрисы в фильме «Drawing Restraint 9» 
        своего тогдашнего мужа Мэттью Барни, саундтрек к которому был выпущен отдельным одноимённым альбомом. 
        В 2010 году Бьорк получила премию «Polar Music Prize» от Шведской королевской академии музыки за её «глубоко 
        личные музыку и слова, её точные аранжировки и её уникальный голос». Всего у артистки более ста наград и двухсот 
        номинаций. Её альбом «Biophilia» (2011) был первым альбомом в формате мобильных приложений и позднее его 
        включили в состав постоянной коллекции Нью-Йоркского музея Современного искусства (MoMA), почти через год там 
        прошла выставка по мотивам творчества Бьорк, которая охватила весь период её сольной карьеры. Издание «Time» 
        включило Бьорк в раздел «иконы» как одну из 100 самых влиятельных людей в мире, назвав её «верховной жрицей 
        искусств», небольшой текст к нему написала Марина Абрамович, утверждая, что «Бьорк учит нас храбрости быть 
        самими собой». Музыкальные критики всегда отстаивали работу Бьорк, восхваляя её инновационный подход к пению и 
        композиторству, её передовое использование электронных битов, прогрессивные музыкальные видео, и прежде всего — 
        её уникальный голос, описывая её как «самого важного и дальновидного музыканта своего поколения».[2][3][4]'''))

    from classifier.classifier import Classifier
    topics_dict = {
        "1": (
            "секс",
            "семья",
            "быт"
        ),

        "2": ("быт", "беларусь",
              "общая_тема_передвижение",
              "общая_тема_Беларусь",
              "общая_тема_Минск"),

        "3": ("общая_тема_Минск", "фестивали",
              "рестораны", "архитектура",
              "кино и искусство в РБ"),

        "4": ("общая_тема_передвижение",
              "общая_тема_Беларусь",
              "общая_тема_Минск",
              "беларусь_государство",
              "беларусь",
              "быт"),

        "5": ("музыка",
              "фестивали",
              "фотография",
              "кино и искусство в РБ",

              ),
        "6": (
            "бизнес"
        ),

        "7": ("бизнес", "тенденции в it", "тенденции в моде",
              "кино и искусство в РБ",
              ),
        "8": ("концерт_спектакль_событие",
              "мировоззрение", "музыка",
              "фестивали"),
        "9": ("архитектура", "фотография",
              "кино и искусство в РБ",
              "мировоззрение"
              ),
        "10": ("секс", "семья", "быт"),
        "11": ("тенденции в it", "мировоззрение"),
        "12": (
            "одежда"
        ),
        "13": (
            "кино и искусство в РБ",
        ),
        "14": (
            "политика_литература",
            "кино и искусство в РБ",
            "мировоззрение"
        ),
        "15": (
            "тенденции в it",
            "интернет_порталы",
            "беларусь"),
        "16": (
            "фотография"
        ),
        "17": (
            "общая_тема_передвижение",
            "фестивали",
        ),
        "18": (
            "беларусь",
            "общая_тема_Беларусь",
            "общая_тема_Минск",
            "быт",
            "политика"
            "беларусь_мир"
        ),
        "19": (
            "общая_тема_Минск",
            "архитектура",
        ),
        "20": (
            "концерт_спектакль_событие",
            "фестивали",
        ),
        "21": (),
        "22": (
            "быт"
        ),
        "23": (
            "общая_тема_Минск",
            "туризм", "бизнес",
            "беларусь_государство",
        ),

        "24": (
            "общая_тема_передвижение",
            "общая_тема_Беларусь",
            "общая_тема_Минск",
            "туризм",
            "беларусь",
            "фестивали",
            "мировоззрение",
        ),

        "25": (
            "общая_тема_передвижение",
            "общая_тема_Беларусь",
            "общая_тема_Минск",
            "туризм",
            "беларусь",
            "фестивали",
            "мировоззрение",
        ),

        "26": (),
        "27": (
            "тенденции в it",
        ),

        "28": (
            "общая_тема_передвижение",
            "общая_тема_Беларусь",
            "общая_тема_Минск",),

        "29": (),

        "30": (
            "интернет_порталы",
            "тенденции в it",
            "общая_тема_Беларусь",
            "общая_тема_Минск"
        ),
        "31": (
            "рестораны",
            "кино и искусство в РБ",
            "туризм",
            "концерт_спектакль_событие",
            "фестивали",
           ),
        "32": (),

        "33": (
            "общая_тема_Беларусь",
            "беларусь_государство",
            "беларусь"
        ),

        "34": (
            "общая_тема_передвижение",
            "общая_тема_Беларусь",
            "общая_тема_Минск",
            "туризм",
            "беларусь"
        ),
    }
    my_classifier = Classifier(topics_dict, topic_destribution)
    print(my_classifier.classify("contents.csv"))


