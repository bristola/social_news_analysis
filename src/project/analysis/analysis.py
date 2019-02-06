from nltk import download
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.stem import WordNetLemmatizer
import re
from stop_words import stop_words
from extra_words import extra_words

# TODO: Emoticons get removed when near a stop word, skewing the results

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


    def get_emoticons_value(self, sentances):
        emoticons = list()
        for sentance in sentances:
            emoticons.extend(re.findall(u'[\U00010000-\U0010ffff]', sentance, flags=re.UNICODE))
        print(emoticons)
        return emoticons


    def get_mood(self, sentances):
        return None


    def run(self, input_type, file_name):
        data = self.get_data(file_name)

        sentiment = 0
        weight_total = 0
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
            emoticon_val = self.get_emoticons_value(sentances)
            mood_val = self.get_mood(sentances)

            sentiment += sentiment_val * weight
            for e in emoticon_val:
                emoticon[e] = 1 if e not in emoticon else emoticon[e] + 1
            mood[mood_val] = 1 if mood_val not in mood else mood[mood_val] + 1

        return sentiment / weight_total, emoticon, mood


a = Analyzer()
# text = "🤬 This is a clown show or what? It is so bad!"
# sentances = a.prepare_data(text)
# # print(sentances)
# # print(a.get_sentiment(sentances))
# print(a.get_emoticons_value(sentances))
sentiment, emoticon, mood = a.run("Twitter", "test.txt")
print(sentiment)
print(emoticon)
print(mood)
