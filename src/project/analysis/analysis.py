from nltk import download
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.stem import WordNetLemmatizer
import json

class Analyzer:

    def __init__(self, extra_words_file='extra_words.json'):
        download('punkt')
        download('wordnet')
        download('vader_lexicon')
        self.lemmatizer = WordNetLemmatizer()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        with open(extra_words_file, 'r') as extra_words:
            words = json.loads(extra_words.read())
            print(words)
            self.sentiment_analyzer.lexicon.update(words)

    def get_sentiment(self, data):
        sentiment_total = 0
        sentances = tokenize.sent_tokenize(data)
        for sentance in sentances:
            lemmas = [self.lemmatizer.lemmatize(word) for word in sentance.split(" ")]
            sentance = ' '.join(lemmas)
            sentiment = self.sentiment_analyzer.polarity_scores(sentance)
            sentiment_total += sentiment['compound']
        return sentiment_total / len(sentances)

a = Analyzer()
a.get_sentiment("This is a clown show or what?")
