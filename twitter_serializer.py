from twitter_api import get_tweets
import json
import os
import uuid

base_folder = 'documents/'

def serialize_tweets():
    # NOTE: Twitter API doesn't allow to filter by language directly.
    tweets = filter(lambda x: x.get('lang') == 'en', get_tweets('biden').get('data'))
    tweets = list(map(lambda x: { 'id': x.get('id'), 'text': x.get('text') }, tweets))

    random_filename = os.path.join(base_folder, f'tweets_{str(uuid.uuid4())}.json')
    with open(random_filename, 'w') as f:
        json.dump(tweets, f)
        print(f'Serialized tweets to {random_filename}')
     
    return tweets
