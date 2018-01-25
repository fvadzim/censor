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
            regulirizers, name, background_topic_number=0):
        self.__phi_matrix = phi_matrix
        self.__topic_matrix = self.__phi_matrix.transpose()
        self.__topic_names = tuple(self.__topic_matrix.index)
        self.__theta_matrix = theta_matrix

        self.__topic_number = phi_matrix.shape[1]  # int
        self.__process_number = process_number  # int
        self.__iterations_via_document = iterations_via_document  # int
        self.__iterations_via_collection = iterations_via_collection  # int
        self.__regulirizers = regulirizers  # dict
        self.__name = name  # str
        self.__background_topic_number = background_topic_number

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

    def get_token_distribution(self, token, modality_num=0):
        try:
            token_distribution = self.__phi_matrix.loc[token]
            if type(token_distribution) == pd.core.frame.DataFrame:
                return token_distribution.iloc[1]
            return token_distribution
        except:
            return np.zeros(self.get_topic_number())

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
        result_topic_vector = sum(
            self.__model.get_token_distribution(token) for token in tokens)
        return result_topic_vector / sum(result_topic_vector)

    def get_similarity(self, distribution_first, distribution_second):
        return cosine(distribution_first, distribution_second)

    def get_most_similar_distribution(self, text):
        text_distribution = self.get_distribution(text)
        most_similar_distribution, similarity_value = (
            self.__model.get_topic_matrix().iloc[0], np.inf,)
        return text_distribution.idxmax()
        '''for topic_name in self.__model.get_topic_names():
            print ("similarity value : {0}".format(similarity_value))
            print("topic name : {0}".format(topic_name))
            print("topic distribuituin :\n {0}".format(self.__model.get_topic_matrix().loc[topic_name],))
            print("get similarity :\n {0}".format( self.get_similarity(
                    self.__model.get_topic_matrix().loc[topic_name],
                    text_distribution) ))
            if self.get_similarity(
                    self.__model.get_topic_matrix().loc[topic_name],
                    text_distribution) < similarity_value:

                most_similar_distribution = \
                    self.__model.get_topic_matrix().loc[topic_name]

                similarity_value = self.get_similarity(
                    most_similar_distribution, text_distribution)'''
        return most_similar_distribution


if __name__ == "__main__":
    model = artm.ARTM(num_topics=27)
    model.load(filename="devided_model_made_properly")
    my_model = Model(
        phi_matrix=model.get_phi(),
        theta_matrix="huy",
        process_number=4,
        iterations_via_collection=10,
        iterations_via_document=10,
        regulirizers={},
        name="first_of_this_class",
        background_topic_number=3
    )
    print((my_model.get_token_distribution("оргазм")))
    topic_destribution = TopicDestribution(my_model)
    print(topic_destribution.get_most_similar_distribution("пизда хуй оргазм секс сексуальный пидор"))

