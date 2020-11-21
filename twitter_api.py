import requests

ENDPOINT = 'https://api.twitter.com/2/tweets/search/recent'

KEY = 'gyv3hz63qIVpa5jUSJT9HZKLF'
SECRET = 'akkuFZpiQtFbA3cZ7E2YbgYsPsJjgNV8iS4YilNRnVX4hvvzgt'
TOKEN = 'AAAAAAAAAAAAAAAAAAAAAIPFJQEAAAAA4rIHOf0dRuH1Tel%2FbOqPZSCjuiE%3DppBOAK3r6pcYg2BpxXXWDF7ZiJKyw8lWCFtRqw3DDhusx1TuZs'

headers = {
    'Authorization': f'Bearer {TOKEN}'
}

def fetch_tweets(search_term):
    query = f'max_results=100&query={search_term}&tweet.fields=lang'

    req = requests.get(f'{ENDPOINT}?{query}', headers=headers)
    return req.json()
