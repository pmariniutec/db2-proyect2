from .tfidf import Index
from .twitter_serializer import get_tweets, get_tweets_files, read_tweets
from .preprocessor import preprocess


def init_index():
    tweets = get_tweets('biden')
    # NOTE: Assume the current list of tweets fits in RAM
    tweets = read_tweets(get_tweets_files())
    dataset_size = len(tweets)

    index = Index(tweets, dataset_size)
    return index
