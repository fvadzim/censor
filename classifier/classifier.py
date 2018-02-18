import csv

def get_csv_rows(reader_csv):
    return [row for row in reader_csv]


class Classifier:
    def __init__(self, topics_dict, topic_destribution):
        self.topics_dict = topics_dict
        self.topic_destribution = topic_destribution

    def classify(self, file_path):
        score = 0.
        with open(file_path, 'r') as csv_file:
            headers = csv_file.readline().strip().split('\t')
            print(headers)
            csv_reader = csv.DictReader(csv_file,
                                        fieldnames=headers,
                                        delimiter='\t')
            documents = get_csv_rows(csv_reader)
            for document in documents:
                if set(self.topics_dict[document["category_id"]]).intersection(
                    set(self.topic_destribution.get_most_similar_distribution(
                        document["content"]
                    ))
                ):
                    score += 1.
            return score / len(documents)

