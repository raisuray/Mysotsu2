import pprint
import mymodule.extract as extract 

class Patent:

    def __init__(self, path):
        
        self.path = path
        self.name = self.path.split('/')[-1]
        self.doc = self.load_file()
        self.doc_experiment = self.load_experiment()
        self.doc_invention = self.load_invention()

    def load_file(self):
        with open(self.path, 'r') as f:
            doc = f.readlines()
        return doc

    def load_experiment(self):
        return extract.exct_experimental_section(self.doc)

    def load_invention(self):
        return extract.exct_invention_section(self.doc)

    def print_experiment(self):
        print("PRINTING 実施例")
        pprint.pprint(self.doc_experiment)

    def print_invention(self):
        print("PRINTING 発明の効果")
        pprint.pprint(self.doc_invention)

    def print_doc(self):
        pprint.pprint(self.doc)

    def print_name(self):
        print("File Name = " + self.name)

