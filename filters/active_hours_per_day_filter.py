import datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))
from filters.utility import convert_timestamp_to_datetime
from external_api.twitter_api import get_tweets_for_user 

QUERY_TWEETS_COUNT_PER_USER = 200

def map_activity_hours(tweets_timestamps):
  activity_map = {}
  for timestamp in tweets_timestamps:
    created_at = convert_timestamp_to_datetime(timestamp)
    created_at_date = created_at.date()
    if created_at_date in activity_map:
      activity_map[created_at_date].add(created_at.hour)
    else:
      activity_map[created_at_date] = set([created_at.hour])
  return activity_map


  
def calculate_average_activity_hours_per_day(activity_dict):#tweets_timestamps):
  total_hours = 0
  for day,hours in activity_dict.items():
    total_hours += len(hours)
  active_days_count = len(activity_dict.keys())
  average_hours_per_day = total_hours / active_days_count
  return active_days_count, average_hours_per_day

def get_tweets_timestamp(tweets):
  timestamps = []
  for tweet in tweets:
    timestamps.append(tweet.created_at)
  return timestamps

def get_user_activity_hours_per_day(user_id,tweets):
  timestamps = get_tweets_timestamp(tweets)
  activity_dict = map_activity_hours(timestamps)
  active_days_count, average_hours_per_day = calculate_average_activity_hours_per_day(activity_dict)
  return {'user_id': user_id, 'active_days_count': active_days_count, 'average_hours_per_day': average_hours_per_day}


def active_hours_per_day_filter(user,start_date=0,end_date=0):
  try:
    tweets = get_tweets_for_user(user['id'],QUERY_TWEETS_COUNT_PER_USER,start_date,end_date)
    if len(tweets) == 0:
      return 0
  except:
    print('Failed to get tweets for user {}'.format(user['id']))
    return 0
  return get_user_activity_hours_per_day(user['id'],tweets)['average_hours_per_day']


