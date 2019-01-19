import twitter
from data_collector import Data_Collector

# pip install python-twitter

# TODO: Retweets are coming through the search and populating data with
# duplicate tweets.

class Twitter_Collector(Data_Collector):

    def __init__(self, key, secret_key, token, token_secret):
        self.api = twitter.Api(consumer_key=key,
                               consumer_secret=secret_key,
                               access_token_key=token,
                               access_token_secret=token_secret,
                               tweet_mode='extended')
        super().__init__('twitter.txt')


    def search(self, topic, max=None, c=100):
        results = self.api.GetSearch(term=topic, max_id=max, count=c, result_type="mixed", lang='en')
        tweets = list()
        min_id = None
        for tweet in results:
            current = dict()
            current['author'] = tweet.user.screen_name
            current['retweets'] = tweet.retweet_count
            current['text'] = tweet.text if tweet.full_text is None else tweet.full_text
            if min_id == None or int(tweet.id) < min_id:
                min_id = int(tweet.id)
            tweets.append(current)
        return tweets, min_id-1


    def create_strings(self, data):
        out_tweets = list()
        for tweet in data:
            out = "%s|%s" % (tweet['retweets'], tweet['text'].replace("\n"," "))
            out_tweets.append(out)
        return out_tweets


    def run(self, topic, iterations):
        min_id = None
        tweets = list()
        for i in range(0, iterations):
            cur_tweets, min_id = self.search(topic, max=min_id)
            tweets.extend(cur_tweets)
        tweets = self.filter_authors(tweets)
        tweets = self.create_strings(tweets)
        self.write_to_file(tweets)
