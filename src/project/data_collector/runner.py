from twitter_collector import Twitter_Collector
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("type", help="Type of data collected. Either 'Twitter' or 'News'.")
parser.add_argument("topic", help="The topic that the data will be searched.")
parser.add_argument("api_key", help="API key that is obtained through a twitter developer account.")
parser.add_argument("api_secret_key", help="API secret key that is obtained through a twitter developer account.")
parser.add_argument("access_token", help="Access token that is obtained through a twitter developer account.")
parser.add_argument("access_token_secret", help="Access token secret that is obtained through a twitter developer account.")

args = parser.parse_args()

if args.type == "Twitter":
    t = Twitter_Collector(args.api_key, args.api_secret_key, args.access_token, args.access_token_secret)
    t.run(args.topic)
elif args.type == "News":
    print("Analyze news articles with search term:", args.topic)
else:
    print("Invalid type argument!")
