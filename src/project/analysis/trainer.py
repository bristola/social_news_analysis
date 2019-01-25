from textblob.classifiers import NaiveBayesClassifier
import pickle

c1 = None

with open('data.json', 'r') as train:
    cl = NaiveBayesClassifier(train, format="json")

with open("trained_classifier.pickle", "wb") as trained_classifier:
    pickle.dump(cl, trained_classifier)
