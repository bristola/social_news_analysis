from nltk import download
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.stem import WordNetLemmatizer
import json
from stop_words import stop_words
from extra_words import extra_words

# The get_sentiment function may need to be combined with other functionalities since we will need to tokenize each time

class Analyzer:

    def __init__(self, extra_words_file='extra_words.json'):
        download('punkt')
        download('wordnet')
        download('vader_lexicon')
        self.lemmatizer = WordNetLemmatizer()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.sentiment_analyzer.lexicon.update(extra_words)


    def remove_stop_words(self, data):
        data = data.lower()
        for stop_word in stop_words:
            data = data.replace(stop_word, "")
        return data

    def prepare_data(self, data):
        in_sentances = tokenize.sent_tokenize(data)
        out_sentances = list()
        for sentance in in_sentances:
            lemmas = [self.lemmatizer.lemmatize(word) for word in sentance.split(" ")]
            # Clean out bad data
            sentance = ' '.join(lemmas)
            out_sentances.append(sentance)
        return out_sentances


    def get_sentiment(self, data):
        sentiment_total = 0
        for sentance in sentances:
            sentiment = self.sentiment_analyzer.polarity_scores(sentance)
            sentiment_total += sentiment['compound']
        return sentiment_total / len(sentances)


a = Analyzer()
# print(a.remove_stop_words("This is a clown show or what?"))
print(a.get_sentiment("This is a clown show or what?"))
