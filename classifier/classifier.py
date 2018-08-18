import csv


def get_csv_rows(reader_csv):
    return [row for row in reader_csv]


class Classifier:
    def __init__(self, topics_dict, topic_distribution):
        self.topics_dict = topics_dict
        self.topic_distribution = topic_distribution

    def classify(self, file_path):
        score = 0.
        with open(file_path, 'r') as csv_file:
            headers = csv_file.readline().strip().split('\t')
            print(headers)
            csv_reader = csv.DictReader(csv_file,
                                        fieldnames=headers,
                                        delimiter='\t')
            documents = get_csv_rows(csv_reader)
            index = 0
            for document in documents:
                if set(self.topics_dict[document["category_id"]]).intersection(
                    set(self.topic_distribution.get_most_similar_distribution(
                        document["content"]
                    ))
                ):
                    score += 1.
                index += 1
                print (score/index )
            return score / len(documents)

