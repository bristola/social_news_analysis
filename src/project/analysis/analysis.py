from nltk import download
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.stem import WordNetLemmatizer
import re
from stop_words import stop_words
from extra_words import extra_words
from emotions import *

class Analyzer:

    def __init__(self):
        download('punkt')
        download('wordnet')
        download('vader_lexicon')
        self.lemmatizer = WordNetLemmatizer()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.sentiment_analyzer.lexicon.update(extra_words)


    def get_data(self, file_name):
        data = None
        with open(file_name, 'r', encoding="utf-8") as data_file:
            data = data_file.readlines()
        return data


    def is_valid_lemma(self, word):
        expression = re.compile(r'(http|https|ftp|ftps)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?')
        if expression.search(word):
            return False
        word = re.sub('[^a-zA-Z\'\d\s]', '', word)
        word = word.lower()
        for stop_word in stop_words:
            if stop_word == word:
                return False
        return True


    def prepare_data(self, data):
        in_sentances = tokenize.sent_tokenize(data)
        out_sentances = list()
        for sentance in in_sentances:
            lemmas = [self.lemmatizer.lemmatize(word) for word in sentance.split(" ")]
            lemmas = [lemma for lemma in lemmas if self.is_valid_lemma(lemma)]
            sentance = ' '.join(lemmas)
            out_sentances.append(sentance)
        return out_sentances


    def get_sentiment(self, sentances):
        sentiment_total = 0
        for sentance in sentances:
            sentiment = self.sentiment_analyzer.polarity_scores(sentance)
            sentiment_total += sentiment['compound']
        return sentiment_total / len(sentances)


    def get_emoticons_value(self, line):
        emoticons = list()
        emoticons.extend(re.findall(u'[\U00010000-\U0010ffff]', line, flags=re.UNICODE))
        return emoticons


    def get_mood(self, sentances):
        moods = {
            "happiness": 0,
            "anxiety": 0,
            "sadness": 0,
            "affection": 0,
            "aggression": 0,
            "expressive": 0,
            "glory": 0
        }
        for sentance in sentances:
            sentance = sentance.lower()
            sentance = re.sub('[^a-zA-Z\'\d\s]', ' ', sentance)
            sentance = re.sub('[ ]{2,}', ' ', sentance)
            for word in sentance.split(" "):
                if word in happiness:
                    moods['happiness'] += 1
                elif word in anxiety:
                    moods['anxiety'] += 1
                elif word in sadness:
                    moods['sadness'] += 1
                elif word in affection:
                    moods['affection'] += 1
                elif word in aggression:
                    moods['aggression'] += 1
                elif word in expressive:
                    moods['expressive'] += 1
                elif word in glory:
                    moods['glory'] += 1
        return moods


    def run(self, input_type, file_name):
        data = self.get_data(file_name)

        weight_total = 0
        sentiment = 0
        emoticon = dict()
        mood = dict()

        for line in data:
            weight = 1
            if input_type == "Twitter":
                columns = line.split("|")
                weight += int(columns[0])
                line = '|'.join(columns[1:])
            weight_total += weight

            sentances = self.prepare_data(line)

            sentiment_val = self.get_sentiment(sentances)
            mood_val = self.get_mood(sentances)
            emoticon_val = self.get_emoticons_value(line)

            sentiment += sentiment_val * weight
            mood[mood_val] = 1 if mood_val not in mood else mood[mood_val] + 1
            for e in emoticon_val:
                emoticon[e] = 1 if e not in emoticon else emoticon[e] + 1

        sentiment /= weight_total
        return sentiment, mood, emoticon


a = Analyzer()
sentiment, mood, emoticon = a.run("Twitter", "test.txt")
print(sentiment)
print(mood)
print(emoticon)
