from twitter_collector import Twitter_Collector
from news_collector import News_Collector
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("type", help="Type of data collected. Either 'Twitter' or 'News'.")
parser.add_argument("topic", help="The topic that the data will be searched.")
parser.add_argument("api_key", help="API key that is obtained through a twitter/newsapi developer account.")
parser.add_argument("api_secret_key", nargs='?', default=None, help="API secret key that is obtained through a twitter developer account.")
parser.add_argument("access_token", nargs='?', default=None, help="Access token that is obtained through a twitter developer account.")
parser.add_argument("access_token_secret", nargs='?', default=None, help="Access token secret that is obtained through a twitter developer account.")

args = parser.parse_args()

if args.type == "Twitter" and None in (args.api_secret_key, args.access_token, args.access_token_secret):
    print("You must have an api_key, api_secret_key, access_token, and access_token_secret when collecting Twitter data")
else:
    if args.type == "Twitter":
        t = Twitter_Collector(args.api_key, args.api_secret_key, args.access_token, args.access_token_secret)
        t.run(args.topic, 25)
    elif args.type == "News":
        t = News_Collector(args.api_key)
        t.run(args.topic, 1)
    else:
        print("Invalid type argument!")
