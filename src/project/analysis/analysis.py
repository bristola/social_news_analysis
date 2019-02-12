from nltk import download
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.stem import WordNetLemmatizer
import re
from words import *

class Analyzer:

    def __init__(self):
        # Download necessary nltk dependancies
        download('punkt')
        download('wordnet')
        download('vader_lexicon')
        # Setup nltk objects
        self.lemmatizer = WordNetLemmatizer()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        # Customize lexicon with extra words
        self.sentiment_analyzer.lexicon.update(extra_words)


    def get_data(self, file_name):
        """
        Gets all data from the specified file including emoticons.
        """
        data = None
        with open(file_name, 'r', encoding="utf-8") as data_file:
            data = data_file.readlines()
        return data


    def is_valid_lemma(self, word):
        """
        Checks if the input word is valid or not. Returns boolean accordingly.
        Filters out any tokens that are links or stop words.
        """
        # Expression for finding links. Return false if one is found
        expression = re.compile(r'(http|https|ftp|ftps)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?')
        if expression.search(word):
            return False
        # Remove anything but alphanumeric, spaces, and '
        word = re.sub('[^a-zA-Z\'\d\s]', '', word)
        word = word.lower()
        for stop_word in stop_words:
            # If input word matches a stop word, return false
            if stop_word == word:
                return False
        return True


    def prepare_data(self, data):
        """
        Inputs a single string that represents a line of data (tweet, news
        article, etc). Breaks string into a list of sentances, and passes each
        sentance through a lemmatizer and validator. Returns a list of prepared
        sentances.
        """
        # Break string into a list of sentances
        in_sentances = tokenize.sent_tokenize(data)
        out_sentances = list()
        for sentance in in_sentances:
            # Turn each word in sentance into its lemma
            lemmas = [self.lemmatizer.lemmatize(word) for word in sentance.split(" ")]
            # Filters out all words that fail the is_valid_lemma function
            lemmas = [lemma for lemma in lemmas if self.is_valid_lemma(lemma)]
            # Joins words back together and add to list
            sentance = ' '.join(lemmas)
            out_sentances.append(sentance)
        return out_sentances


    def get_sentiment(self, sentances):
        """
        Iterates over input list of sentances. Gets sentiment of each sentance
        and returns the average sentiment.
        """
        sentiment_total = 0
        # Add each sentances combined sentiment to a total tally
        for sentance in sentances:
            sentiment = self.sentiment_analyzer.polarity_scores(sentance)
            sentiment_total += sentiment['compound']
        return sentiment_total / len(sentances)


    def get_emoticons_value(self, line):
        """
        Inputs a string and returns a list of all emoticons that are found.
        """
        emoticons = list()
        # Finds any substring which represents an emote
        emoticons.extend(re.findall(u'[\U00010000-\U0010ffff]', line, flags=re.UNICODE))
        return emoticons


    def get_mood(self, sentances):
        """
        Iterates over each sentance and counts the number of words that are in
        each of the seven emotion categories. Returns dictionary of results.
        """
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
            # Clean data for analysis
            sentance = re.sub('[^a-zA-Z\'\d\s]', ' ', sentance)
            sentance = re.sub('[ ]{2,}', ' ', sentance)
            # Match words to correct category
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
        """
        Runs analytics; takes all the data from the specified file, collects
        sentiment, emotional, and emoticon data. Stores results into
        dictionaries and returns them.
        """
        data = self.get_data(file_name)

        sentiment = dict()
        mood = dict()
        emoticon = dict()

        for line in data:
            weight = 1
            # Twitter data has a weight defined before the |
            if input_type == "Twitter":
                columns = line.split("|")
                weight += int(columns[0])
                # Everything but the weight at the beginning
                line = '|'.join(columns[1:])

            # Prepare data for analysis
            sentances = self.prepare_data(line)

            # Perform analysis
            sentiment_val = self.get_sentiment(sentances)
            mood_val = self.get_mood(sentances)
            emoticon_val = self.get_emoticons_value(line)

            # Add each sentiment value to a dictionary along with its weight
            sentiment[sentiment_val] = weight if sentiment_val not in sentiment else sentiment[sentiment_val] + weight
            # Add results to mood totals
            for m, count in mood_val.items():
                mood[m] = count if m not in mood else mood[m] + count
            # Add results to emote totals
            for e in emoticon_val:
                emoticon[e] = 1 if e not in emoticon else emoticon[e] + 1

        return sentiment, mood, emoticon
