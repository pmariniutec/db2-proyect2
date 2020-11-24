import json
import os
import numpy as np

from nltk.tokenize import word_tokenize
from collections import Counter
from .tfidf import Index
from .twitter_serializer import get_tweets
from .preprocessor import preprocess


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


def init_index():
    # tweets = get_tweets('biden')
    # NOTE: Assume the current list of tweets fits in RAM?
    tweets = read_tweets(get_tweets_files())
    dataset_size = len(tweets)

    index = Index(tweets, dataset_size)
    # q = index.search(10, "Trump is no longer a puppet")
    # print(q)
    return index
