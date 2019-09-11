
from neo4j import GraphDatabase
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))
import credentials
from db.redis_cache import retrieve_headlines
from external_api.twitter_api import twitter_search_users_by_headlines, twitter_search_tweets_by_headlines

GRAPHENEDB_BOLT_USER = os.environ.get('GRAPHENEDB_BOLT_USER')
GRAPHENEDB_BOLT_PASSWORD = os.environ.get('GRAPHENEDB_BOLT_PASSWORD')
GRAPHENEDB_BOLT_URL = os.environ.get('GRAPHENEDB_BOLT_URL')

driver = GraphDatabase.driver(
    GRAPHENEDB_BOLT_URL, auth=(GRAPHENEDB_BOLT_USER, GRAPHENEDB_BOLT_PASSWORD))

session = driver.session()


def add_user_node(tx, user, source):
    # tx.run("MERGE (b:Bot {screen_name: $user.screen_name, id: $user.id, age: $user.created_at, score: $user.score, average_tweets: $user.average_tweets, followers: $user.followers, total_tweets: $user.total_tweets, status: $user.status}) "
    #     #    "MERGE (s:Source {source: $source.source, content: $source.content}) "
    #        "MERGE (b)-[:TWEETED {created_at: $text_string.created_date}]->(t) ",
    #        user=user)
    text_source = "MERGE (s:Source { text: $source }) "
    tx.run("MERGE (a:User {screen_name: $user['screen_name'], id: $user['id'], created_at: $user['created_at'], followers_count: $user['followers_count'], statuses_count: $user['statuses_count']})"#, score: $user['score'], average_tweets: $user['average_tweets'] status: $user['status']}) ",
           f"{text_source}"
           "MERGE (a)-[:TWEETED]->(s)",
           user=user, source=source)


def add_text_node(tx, source):
    tx.run("MERGE (s:Source {source: $source.source, content: $source.content}) ",
           source=source)

def add_hashtag_node(tx, source):
    tx.run("MERGE (s:Source {source: $source.source, content: $source.content}) ",
           source=source)

def add_relationship_node(tx, args):
    pass

def get_bots_and_following_relationships(tx):
    # user_statement = "MATCH (u:User) RETURN u"
    # build_relationships = "MATCH (u)-[:FOLLOWING]->(u) RETURN u"
    labels_data = get_bots(tx)
    relationships_data = get_relationships(tx)
    return template_function(labels_data, relationships_data)
    # label = [for label in labels_data]
    pass

def retrieve_all_data(tx):
    statement = "MATCH (n) RETURN n "
    for record in tx.run(statement):
        return record

def retrieve_user(tx, user_id):
    statement = "MATCH (a:User { id: {user_id} }) RETURN a"
    for record in tx.run(statement, user_id=user_id):
        return record

def retrieve_text_source(tx, text):
    statement = "MATCH (a:Text { text: {text} }) RETURN a"
    for record in tx.run(statement, text=text):
        return record
        
def retrieve_hashtag(tx, hashtag):
    statement = "MATCH (a:Hashtag { text: {text} }) RETURN a"
    for record in tx.run(statement, text=hashtag):
        return record

def get_oldest(tx):
    statement = "MATCH (u:User) RETURN ORDER BY u.created_at DESC LIMIT 1"
    pass

def get_bots(tx):
    records = tx.run("MATCH (u:User) RETURN u.screen_name as screen_name, u.id as id, u.created_at as created_at, u.followers_count as followers_count, u.statuses_count as statuses_count")#u.score as score, u.status as status, u.average_tweets as average_tweets")
    users = []
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
        # for i in record.items()[0][1].items():
        #     print(i[0], i[1])
    # something = [i['n'].items() for i in records]
    # for some in something:
    #     print(some.value())
    # for record in tx.run("MATCH (n) RETURN n"):
    #     for i, j in iter(record['n']):
    #         print(j)
        

def store_data(tx, function_name, data):
    function = {
        'user': add_user_node,
        'text': add_text_node,
        'hashtag': add_hashtag_node,
        'relationship': add_relationship_node
    }
    function[function_name](data)
    # session.write_transaction(element['type'], element['data'])

    # with driver.session() as session:
    #    users = retrieve_users()
    #    print(users)
    #    for user in users:
    #        print(user)
    #        session.write_transaction(add_node_user, user['screen_name'])
    #    session.read_transaction(print_nodes)

def relationships_data(tx):
    
    tx.run("MERGE (b)-[:TWEETED {created_at: $text_string.created_date}]->(t) ",)

def template_function(labels_data, relationships_data):
    return {
        "labels": labels_data,
        "relationships": relationships_data
    }

headlines = retrieve_headlines()
headlines_search = []
print(headlines)
# for headline in headlines:
#     headlines_search.append(headline['title'])
tweeted_headlines = twitter_search_tweets_by_headlines(headlines)
users = twitter_search_users_by_headlines(tweeted_headlines)
# print(users[0])
for user in users:
    session.write_transaction(add_user_node, user[0], user[1])


# print(session.read_transaction(print_nodes))