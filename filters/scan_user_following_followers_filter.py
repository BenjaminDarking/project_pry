import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))
#from users_filter import run_filters, SUSPECTED_BOT_SCORE
from external_api.twitter_api import get_user_following_list, get_user_followers_list, get_user
#from db.graphdb import create_node
#from db.redis_cache import retrieve_users

# TODO: due to missing implementaions inspect_user_following)followers was not testes

def get_user_following_followers_ids(user_id):
  following_ids = get_user_following_list(user_id)
  followers_ids = get_user_followers_list(user_id)
  return following_ids, followers_ids

#def inspect_user_following_followers_filter(user):
#  user_id = user['id']
#  following_ids, followers_ids = get_user_following_followers_ids(user_id)
#  
#  # TODO: decide what data to save for users and relationship
#  
#  for followed_id in following_ids: # The users the user is following 
#    if score_user(followed_id) > SUSPECTED_BOT_SCORE:
#      followed = get_user(followed_id)
#      create_node({'type': 'user', 'data': {'screen_name': followed['screen_name'], 'id': followed_id}})
#      create_node({'type': 'relationship', 'data':{'type':'FOLLOWING', 'direction':[user_id, followed_id], 'user': user, 'followed': followed}})
#
#  for follower_id in followers_ids:
#    if score_user(follower_id) > SUSPECTED_BOT_SCORE:
#      follower = get_user(follower_id)
#      create_node({'type': 'user', 'data': {'screen_name': follower['screen_name'], 'id': follower_id}})
#      create_node({'type': 'relationship', 'data':{'type':'FOLLOWING', 'direction': [follower_id, user_id], 'user': user, 'follower': follower}})
#
def bot_following_ratio_filter():
  pass

def bot_followers_ratio_filter():
  pass

def test_filter():
  users = retrieve_users()
  print(get_user_following_followers_ids(users[0]['id']))
