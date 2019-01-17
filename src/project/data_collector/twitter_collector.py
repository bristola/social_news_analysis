import twitter
from data_collector import Data_Collector
import time

class Twitter_Collector(Data_Collector):

    def __init__(self, key, secret_key, token, token_secret):
        self.api = twitter.Api(consumer_key=key,
                               consumer_secret=secret_key,
                               access_token_key=token,
                               access_token_secret=token_secret)


    def search(self, topic, max=None, c=100):
        results = self.api.GetSearch(term=topic, max_id=max, count=c, result_type="recent", lang='en')
        tweets = list()
        min_id = None
        for tweet in results:
            current = dict()
            current['favorites'] = tweet.favorite_count
            current['retweets'] = tweet.retweet_count
            current['text'] = tweet.text
            current['user'] = tweet.user.screen_name
            current['id'] = tweet.id
            if min_id == None or int(tweet.id) < min_id:
                min_id = int(tweet.id)
            tweets.append(current)
        return tweets, min_id-1


    def run(self, topic, iterations):
        min_id = None
        tweets = list()
        for i in range(0, iterations):
            cur_tweets, min_id = self.search(topic, max=min_id)
            tweets.extend(cur_tweets)

        # TODO: Should I gather the most popular tweets or the most recent?
        # TODO: Check to make sure their is no repeat user tweet
        # TODO: Maybe take into account the likes and retweets
        # TODO: Write it to a file
