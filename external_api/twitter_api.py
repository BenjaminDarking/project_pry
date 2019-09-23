import twitter
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))
import credentials

# Init
try:
  API_CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
  API_CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
  API_ACCESS_TOKEN_KEY = os.environ.get('ACCESS_TOKEN_KEY')
  API_ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')


  api = twitter.Api(consumer_key=(API_CONSUMER_KEY),
                  consumer_secret=(API_CONSUMER_SECRET),
                  access_token_key=(API_ACCESS_TOKEN_KEY),
                  access_token_secret=(API_ACCESS_TOKEN_SECRET),
                  sleep_on_rate_limit=True)
except Exception as e:
  print('Failed to connect to Twitter API with {}'.format(e))

DEFAULT_RETURNED_TWEETS = 200


def twitter_search_tweets_by_headlines(headlines, count=DEFAULT_RETURNED_TWEETS):
    results = []
    for headline in headlines:
        query_result = api.GetSearch(
            term=headline['title'], count=count, return_json=True)
        results.append({'source': headline, 'results': query_result})
    return results



def run_twitter_query(headlines):
  tweeted_headlines = twitter_search_tweets_by_headlines(headlines)
  users_and_sources = get_users_from_tweets(tweeted_headlines)
  store_users(users_and_sources)
  return users_and_sources

def get_users_from_tweets(source_and_tweets):
    users_with_source = []
    for source_with_results in source_and_tweets:
        for tweet in source_with_results['results']['statuses']:
            user = ({'source': source_with_results['source'],
                     'source_type': 'news-headline',
                     'screen_name': tweet['user']['screen_name'],
                     'id': tweet['user']['id'],
                     'urls': tweet['entities']['urls'],
                     'verified': tweet['user']['verified'],
                     'protected': tweet['user']['protected'],
                     'created_at': tweet['user']['created_at'],
                     'statuses_count': tweet['user']['statuses_count'],
                     'followers_count': tweet['user']['followers_count'],
                     'description': tweet['user']['description']})
            if len(user.keys()) > 0:
                users_with_source.append(user)
    return users_with_source


def get_tweets_for_user(user_id, count, start_date=0, end_date=0):
  return api.GetUserTimeline(user_id=user_id, count=count)


def get_user_following_list(attribute,value):
  if attribute == 'user_id':
    return api.GetFriendIDs(user_id=value)
  else:
    return api.GetFriendIDs(screen_name=value)


def get_user_followers_list(attribute,value):
   if attribute == 'user_id':
    return api.GetFollowerIDs(user_id=value)
  else:
    return api.GetFollowerIDs(screen_name=value)


def get_user(user_id):
  return api.GetUser(user_id=user_id, return_json=True)

def get_user_by_name(screen_name):
  return api.GetUser(screen_name=screen_name, return_json=True)


#run_twitter_query()
