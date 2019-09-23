import json
from flask import Flask, Response
#from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from external_api.twitter_api import run_twitter_query
from external_api.news_api import get_headlines
from user_classification import classify_users
#import credentials

def bot_search():
  print("Scheduler is alive!")
  headlines = get_headlines()
  print(headlines)
  users = run_twitter_query(headlines)
  print(users)
  classify_users(users,['tweets_per_day_ratio', 'bot_bio','hours_per_day','timeline_hashtags','retweets_ratio','fake_news'],('knn',3))



app = Flask(__name__)
#sched = BackgroundScheduler(daemon=True)
sched = BlockingScheduler()
sched.add_job(bot_search,'interval',minutes=55)
sched.start()



@app.route('/')
def dummy_node():
  node = json.dumps({
    'label':{'User':[
      {'screen_name': 'Hal', 'id':'1', 'total_tweets':'1200000'},
      {'screen_name': 'Dave', 'id':'2', 'total_tweets':'12'},
      {'screen_name': 'Ben', 'id':'3', 'total_tweets':'120000'},
      {'screen_name': 'MarvinTheParanoidAndroid', 'id':'4', 'total_tweets':'1200'},
      {'screen_name': 'ArthurDent', 'id':'5', 'total_tweets':'130000'},
      {'screen_name': 'FordPrefect', 'id':'6', 'total_tweets':'5200000'}
    ]},
    'relationships':{'FOLLOWING':[
        {'source':'1', 'destination':'2','created_at':'1968-02-29', 'bidirectional':'True'},
        {'source':'5', 'destination':'6','created_at':'1981-03-19', 'bidirectional':'False'},
        {'source':'4', 'destination':'6','created_at':'1982-02-01', 'bidirectional':'False'},
        {'source':'3', 'destination':'4','created_at':'2019-10-09', 'bidirectional':'False'}
      ]}
      }
    )
  res = Response(node)
  res.headers['Content-Type'] = 'application/json' 
  #print(node)
  return node

if __name__ == '__main__':
  try:
    app.run()
  except:
    print('killing scheduler')
    sched.shutdown()
