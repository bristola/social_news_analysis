import twitter
from data_collector import Data_Collector

# pip install python-twitter

class Twitter_Collector(Data_Collector):

    def __init__(self, key, secret_key, token, token_secret):
        self.api = twitter.Api(consumer_key=key,
                               consumer_secret=secret_key,
                               access_token_key=token,
                               access_token_secret=token_secret,
                               tweet_mode='extended')
        super().__init__('data.txt')


    def search(self, topic, max=None, c=100):
        """
        Takes the input topic and collects next 100 tweets based on max
        paramter. Ensures we start at last collected tweet to avoid duplicates.
        Collects text, retweets, and author.
        """
        # Searches for tweets
        results = self.api.GetSearch(term=topic, max_id=max, count=c, result_type="mixed", lang='en')
        tweets = list()
        min_id = None
        for tweet in results:
            # Tries to find the oldest tweet ID
            if min_id == None or int(tweet.id) < min_id:
                min_id = int(tweet.id)
            current = dict()
            # If tweet is a retweet, use the retweet data object.
            tweet = tweet if tweet.retweeted_status is None else tweet.retweeted_status
            current['author'] = tweet.user.screen_name
            current['retweets'] = tweet.retweet_count
            current['text'] = tweet.text if tweet.full_text is None else tweet.full_text
            tweets.append(current)
        # Returns twitter data and the oldest ID to start at next time.
        return tweets, min_id-1


    def create_strings(self, data):
        """
        Takes input data and gets it into a format which will be written to a
        file.
        """
        out_tweets = list()
        for tweet in data:
            out = "%s|%s" % (tweet['retweets'], tweet['text'].replace("\n"," "))
            out_tweets.append(out)
        return out_tweets


    def run(self, topic, iterations):
        """
        Runs the collection of tweets on the given topic the input number of
        times. Each time will make sure that it is a unique set of tweets.
        """
        min_id = None
        tweets = list()
        for i in range(0, iterations):
            # Gets twitter data and oldest tweet id for next search
            cur_tweets, min_id = self.search(topic, max=min_id)
            tweets.extend(cur_tweets)
        # Prepares and writes data to file
        tweets = self.filter_authors(tweets)
        tweets = self.create_strings(tweets)
        self.write_to_file(tweets)
