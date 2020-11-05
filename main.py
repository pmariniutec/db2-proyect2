from twitter_serializer import serialize_tweets
from nltk.tokenize import word_tokenize
from preprocessor import preprocess
from collections import Counter
import json
import os
import numpy as np
from tfidf import build_index, search


documents_dir = f'{str(os.getcwd())}/documents/'


def get_tweets_files():
    return [os.path.join(documents_dir, f) for f in os.listdir(documents_dir) if os.path.isfile(os.path.join(documents_dir, f))]


def read_tweets(files):
    data = []
    for f in files:
        with open(f) as infile:
           obj = json.load(infile)
           for tweet in obj:
               data.append(tweet.get('text'))
    return data


def main():
    # tweets = serialize_tweets()
    tweets = read_tweets(get_tweets_files())
    dataset_size = len(tweets)

    index = build_index(tweets, dataset_size)
    q = search(10, "Trump is no longer a puppet")
    print(q)

    # TODO: DESIRED API
    '''
    index = Index()
    q = index.search(10, "Trump is no longer a puppet")
    print(q)
    '''



if __name__ == '__main__':
    main()
