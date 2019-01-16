import twitter
from data_collector import Data_Collector

class Twitter_Collector(Data_Collector):

    def __init__(self, key, secret_key, token, token_secret):
        self.api = twitter.Api(consumer_key=key,
                               consumer_secret=secret_key,
                               access_token_key=token,
                               access_token_secret=token_secret)


    def search(self, topic, max=None, c=100):
        results = self.api.GetSearch(term=topic, max_id=max, count=c, result_type="recent", lang='en')
        tweets = list()
        for tweet in results:
            current = dict()
            current['favorites'] = tweet.favorite_count
            current['retweets'] = tweet.retweet_count
            current['text'] = tweet.text
            current['user'] = tweet.user.screen_name
            tweets.append(current)
        return tweets


    def run(self, topic):
        # TODO: Max API query is 100 tweets. Need to iterate as many times as
        # the API will allow. Each time, query for the most recent tweets, and
        # take the lowest ID from the data. Use this ID as the max_id for the
        # next iteration.
        return
