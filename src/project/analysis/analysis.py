import pickle
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

cl = None

with open("trained_classifier.pickle", "rb") as trained_classifier:
    print(trained_classifier)
    cl = pickle.load(trained_classifier)

print(cl.classify("This is awesome!"))

# BREAK INTO BLOBS

# TOKENIZE

# LEMMATIZE

# CLASSIFY
