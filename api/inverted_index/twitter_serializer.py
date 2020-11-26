import json
import os
from .twitter_api import fetch_tweets


documents_dir = f'{str(os.getcwd())}/documents/'


def get_tweets(search_term):
    # NOTE: Twitter API doesn't allow to filter by language directly, so we do it here.
    tweets = filter(lambda x: x.get('lang') == 'en', fetch_tweets(search_term).get('data'))
    tweets = list(map(lambda x: { 'id': x.get('id'), 'text': x.get('text') }, tweets))

    for tweet in tweets:
        filename = os.path.join(documents_dir, f"tweet_{tweet.get('id')}.json")
        with open(filename, 'w') as out:
            json.dump(tweet, out)

    print(f'Serialized {len(tweets)} tweets')

    return tweets


def get_tweets_files():
    return [os.path.join(documents_dir, f) for f in os.listdir(documents_dir) if os.path.isfile(os.path.join(documents_dir, f))]


def read_tweets(files):
    data = []
    for f in files:
        with open(f) as infile:
            tweet = json.load(infile)
            data.append({'text': tweet.get('text'), 'id': tweet.get('id')})
    return data


def get_tweets_by_ids(tweet_ids):
    data = []
    for tweet_id in tweet_ids:
        filename = os.path.join(documents_dir, f"tweet_{tweet_id}.json")
        try:
            with open(filename, 'r') as tweet:
                data.append(json.load(tweet))
        except FileNotFoundError:
            continue
    return data
