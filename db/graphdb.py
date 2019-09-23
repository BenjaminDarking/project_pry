from neo4j import GraphDatabase
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))
#import credentials
#from db.redis_cache import retrieve_headlines, retrieve_users
#from external_api.twitter_api import run_twitter_query

GRAPHENEDB_BOLT_USER = os.environ.get('GRAPHENEDB_BOLT_USER')
GRAPHENEDB_BOLT_PASSWORD = os.environ.get('GRAPHENEDB_BOLT_PASSWORD')
GRAPHENEDB_BOLT_URL = os.environ.get('GRAPHENEDB_BOLT_URL')
#try:
#  driver = GraphDatabase.driver(
#    GRAPHENEDB_BOLT_URL, auth=(GRAPHENEDB_BOLT_USER, GRAPHENEDB_BOLT_PASSWORD))
#  session = driver.session()
#  print('Created session')
#except Exception as e:
#  print('Failed to connect to DB {}'.format(e))
#

## ---------------- ADDING USERS TO THE DB ----------------
# As we only have four methods by which a user should enter
# the project's database, i'm breaking those functions out
# below for easy reading, although we've included a wrapping
# function for simple use throughout the application.

def store_user(user):
    function = {
        'headline': add_user_node_source_headline(user),
        'text': add_user_node_source_text(user),
        'hashtag': add_user_node_source_hashtag(user),
        'user': add_user_node_source_user(user)
    }
    function[source](user)

def add_user_node_source_headline(user):
    source = user['source']
    with driver.session() as session:
        session.run("MERGE (a:User {screen_name: $user['screen_name'], id: $user['id'], created_at: $user['created_at'], followers_count: $user['followers_count'], statuses_count: $user['statuses_count']}) "#, score: $user['score'], average_tweets: $user['average_tweets'] status: $user['status']}) ",
                    "MERGE (s:Source {title: $source['title'], published_at: $source['published_at'], publisher: $source['publisher'], url: $source['url']}) "
                    "MERGE (a)-[:TWEETED]->(s) ",
                    user=user, source=source)

def add_user_node_source_text(user):
    source = user['source']
    with driver.session() as session:
        session.run("MERGE (a:User {screen_name: $user['screen_name'], id: $user['id'], created_at: $user['created_at'], followers_count: $user['followers_count'], statuses_count: $user['statuses_count']}) "#, score: $user['score'], average_tweets: $user['average_tweets'] status: $user['status']}) ",
                    "MERGE (s:Source {title: $source['title'], published_at: $source['published_at'], publisher: $source['publisher'], url: $source['url']}) "
                    "MERGE (a)-[:TWEETED]->(s) ",
                    user=user, source=source)

def add_user_node_source_hashtag(user):
    source = user['source']
    with driver.session() as session:
        session.run("MERGE (a:User {screen_name: $user['screen_name'], id: $user['id'], created_at: $user['created_at'], followers_count: $user['followers_count'], statuses_count: $user['statuses_count']}) "#, score: $user['score'], average_tweets: $user['average_tweets'] status: $user['status']}) ",
                    "MERGE (s:Source {title: $source['title'], published_at: $source['published_at'], publisher: $source['publisher'], url: $source['url']}) "
                    "MERGE (a)-[:TWEETED]->(s) ",
                    user=user, source=source)

def add_user_node_source_user(user):
    source = user['source']
    with driver.session() as session:
        session.run("MERGE (a:User {screen_name: $user['screen_name'], id: $user['id'], created_at: $user['created_at'], followers_count: $user['followers_count'], statuses_count: $user['statuses_count']}) "#, score: $user['score'], average_tweets: $user['average_tweets'] status: $user['status']}) ",
                    "MERGE (s:Source {title: $source['title'], published_at: $source['published_at'], publisher: $source['publisher'], url: $source['url']}) "
                    "MERGE (a)-[:TWEETED]->(s) ",
                    user=user, source=source)

## ---------------- ADDING RELATIONSHIPS TO THE DB ----------------
# These methods should be run in the event where in case there may
# be new unlinked bots to sources, or bots to other bots we can 
# update the db to reflect these relationships. I.e we can run the 
# following filter and see whether any of the following/followers 
# match a suspected bot in the database and then denote their
# relationship to each other.

def set_bot_to_bot_relationships(first_user, second_user, bidirectional):
    # create a link between two nodes to denote that either one or 
    # both is following the other. Must be passed with the bidirectional
    # boolean - if false the first_user will be denoted as FOLLOWING the
    # second user, otherwise they will be noted as following each other.
    # I have used first and second user here as it is clearer than following
    # and follower I believe, may be wrong here. 
    first_user_assignment = "MATCH (f:User {id: $first_user['id']})"
    second_user_assingment = "MATCH (s:User {id: $second_user['id']})"
    if bidirectional == True:
        build_relationships = "MATCH (f)<-[:FOLLOWING]->(s)"
    else:
        build_relationships = "MATCH (f)-[:FOLLOWING]->(s)"
    
    with driver.session() as session:
        session.run(first_user_assignment + 
                    second_user_assingment +
                    build_relationships, first_user=first_user, second_user=second_user
                    )
    

## ---------------- RETRIEVING DATA FROM THE DB ----------------
# These methods allow us to perform the necessescary operations to
# retrieve users, sources and stats from the db. 

def retrieve_all_data():
    # careful calling this, it can be a very large query / response
    # perhaps you actually need to retrieve only a single node or
    # cluster?
    with driver.session() as session:
        for record in session.run("MATCH (n) RETURN n "):
            return record

def retrieve_user(user):
    with driver.session() as session:
        for record in session.run("MATCH (u:User) RETURN u.screen_name as screen_name, u.id as id, u.created_at as created_at, u.followers_count as followers_count, u.statuses_count as statuses_count"):
            user = {
                "User": {
                    "screen_name": record["screen_name"],
                    "id": record["id"],
                    "created_at": record["created_at"],
                    "score": record["score"],
                    "average_tweets": record["average_tweets"],
                    "followers_count": record["followers_count"],
                    "statuses_count": record["statuses_count"]
                }
            }
        return user

def retrieve_all_users():
    with driver.session() as session:
        users = []
        records = session.run("MATCH (u:User) RETURN u.screen_name as screen_name, u.id as id, u.created_at as created_at, u.followers_count as followers_count, u.statuses_count as statuses_count")#u.score as score, u.status as status, u.average_tweets as average_tweets")
        for record in records:
            user = {
                "User": {
                    "screen_name": record["screen_name"],
                    "id": record["id"],
                    "created_at": record["created_at"],
                    "score": record["score"],
                    "average_tweets": record["average_tweets"],
                    "followers_count": record["followers_count"],
                    "statuses_count": record["statuses_count"]
                    # "status": record["status"]
                }
            }
            users.append(user)
    return users

def retrieve_text_source(text):
    statement = "MATCH (a:Text { text: {text} }) RETURN a.text as text"
    with driver.session() as session:
        for record in session.run(statement, text=text):
            return record
        
def retrieve_hashtag(hashtag):
    statement = "MATCH (a:Hashtag { text: {text} }) RETURN a.text as text, a.tending as trending"
    with driver.session() as session:
        for record in session.run(statement, text=hashtag):
            return record

def retrieve_headline(url):
    statement = "MATCH (a:Headline { url: {text} }) RETURN a.title as title, a.publisher as publisher, a.published_at as published_at, a.url as url"
    with driver.session() as session:
        for record in session.run(statement, text=url):
            headline = {
                'title': record['title'],
                'publisher': record['publisher'],
                'published_at': record['published_at'],
                'url': record['url']
            }
            return headline

