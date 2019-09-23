import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))
#import credentials
from user_classification import run_filters_on_users
from external_api.twitter_api import get_user_by_name, get_user_following_list, get_user
from db.postgresql_storage import store_classified_set

def get_bots_info(file_name,bots=True):
  bots=[]
  with open(file_name,'r') as f:
    with open('failed_bots_log.txt','a') as log:
      count = 0
      for bot_name in f.readlines():
        if count <= 200:
          try:
            res = get_user_by_name(bot_name)
            bots.append(res)
          except:
            log.write('{}\n'.format(bot_name))
            print('failed with user {}'.format(bot_name))
          finally:
            count+=1
        else:
          #print('\n\nRUNNING FILTERS NOW\n\n')
          results = run_filters_on_users(bots,['tweets_per_day_ratio', 'bot_bio','hours_per_day','timeline_hashtags','retweets_ratio','fake_news'])
          store_classified_set(results)
          count = 0
          bots = []
      if len(bots) > 0:
        #print('\n\nRUNNING FILTERS NOW\n\n')
        results = run_filters_on_users(bots,['tweets_per_day_ratio', 'bot_bio','hours_per_day','timeline_hashtags','retweets_ratio','fake_news'])
        store_classified_set(results)


def get_humans_info(screen_name,bots=False):
  following = get_user_following_list('screen_name',screen_name)
  #print('got list: len={}'.format(len(following)))
  humans = []
  count = 0
  for friend_id in following:
    if count <= 200:
      res = get_user(friend_id)
      humans.append(res)
      count += 1
    else:
      results = run_filters_on_users(humans,['tweets_per_day_ratio', 'bot_bio','hours_per_day','timeline_hashtags','retweets_ratio','fake_news'],False)
      store_classified_set(results)
      count = 0
      humans = []
  if len(humans) > 0:
    results = run_filters_on_users(humans,['tweets_per_day_ratio', 'bot_bio','hours_per_day','timeline_hashtags','retweets_ratio','fake_news'],False)
    store_classified_set(results)
    
def get_user_info(screen_name,bots=False):
  humans=[]
  res = get_user_by_name(screen_name)
  humans.append(res)
  results = run_filters_on_users(humans,['tweets_per_day_ratio', 'bot_bio','hours_per_day','timeline_hashtags','retweets_ratio','fake_news'],False)
  return results

try:
  #get_bots_info('last-bots.txt',True)
  #get_humans_info('northern_tester',False)
  #print(get_user_info('screen_name',False))
except Exception as e:
  print('Failed prepping humans with: {}'.format(e))

