import json
import re

def write_to_trainer(data, file_name="training_data.json"):
    """Data must be a dictionary"""
    with open(file_name, 'a') as training:
        json.dump(data, training)


def get_next_tweet(file_name="tweets.txt"):
    with open(file_name, 'r', encoding="utf8") as tweets:
        for line in tweets:
            try:
                tweet = line.split("|")[1].strip()
                tweet = re.sub('(http|https|ftp|ftps)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?',  ' ', tweet)
                tweet = re.sub('[^a-zA-Z\d\s]', ' ', tweet)
                tweet = tweet.replace("amp", " ")
                tweet = re.sub('[ ]{2,}', ' ', tweet)
                yield tweet
            except Exception as e:
                pass


def get_user_response(tweet):
    types = ['neg2','neg1','neutral','pos1','pos2','exit','pass']
    response = None
    while response is None or response not in types:
        response = input("Please enter one of the following: %s: " % (str(types)))
    return response


def main():
    output = dict()
    for tweet in get_next_tweet():
        print("\n",tweet)
        response = get_user_response(tweet)
        if response == 'exit':
            break
        if response == 'pass':
            continue
        output[tweet] = response
    write_to_trainer(output)


if __name__ == '__main__':
    main()
