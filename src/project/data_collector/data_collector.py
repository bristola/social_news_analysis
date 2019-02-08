from abc import ABC, abstractmethod

class Data_Collector(ABC):

    def __init__(self, out_file):
        self.output = out_file


    def write_to_file(self, data):
        """
        Takes all the list of data and writes it to a new file.
        """
        with open(self.output, 'w+', encoding="utf-8") as f:
            f.write("\n".join(data))


    def filter_authors(self, data):
        """
        Takes the input list of data, and removes all data that has an author
        that is already found in the data.
        """
        authors = list()
        out_data = list()
        for d in data:
            # If it is a new author, add it to output and add author to list
            if not d['author'] in authors:
                authors.append(d['author'])
                out_data.append(d)
        return out_data


    @abstractmethod
    def search(self, topic, max=None, c=100):
        pass


    @abstractmethod
    def create_strings(self, data):
        pass


    @abstractmethod
    def run(self, topic, iterations):
        pass
