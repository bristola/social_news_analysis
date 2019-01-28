import json

def write_to_trainer(data, file_name="training_data.json"):
    """Data must be a dictionary"""
    with open(file_name, 'w+') as training:
        json.dump(data, training)


def get_next_tweet(file_name="tweets.txt"):
    with open(file_name, 'r') as tweets:
        for line in tweets:
            try:
                tweet = line.split("|")[1].strip()
                yield tweet
            except Exception as e:
                pass


def get_user_response(tweet):
    types = ['neg2','neg1','neutral','pos1','pos2']
    response = None
    while response is None or response not in types:
        response = input("Please enter one of the following: %s: " % (str(types)))
    return response


def main():
    output = dict()
    for tweet in get_next_tweet():
        print("\n",tweet)
        response = get_user_response(tweet)
        output[tweet] = response
    write_to_trainer(output)


if __name__ == '__main__':
    main()
