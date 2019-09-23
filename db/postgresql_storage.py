import psycopg2
import os
import sys
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))
#import credentials

try:

  PGHOST=os.environ.get('PGHOST')
  PGDATABASE=os.environ.get('PGDATABASE')
  PGUSER=os.environ.get('PGUSER')
  PGPASSWORD=os.environ.get('PGPASSWORD')

  connection_string = "host="+ PGHOST +" port="+ "5432" +" dbname="+ PGDATABASE +" user=" + PGUSER \
    +" password="+ PGPASSWORD
  connection = psycopg2.connect(connection_string)
  print("Connected to Postgres DB")

  cursor = connection.cursor()

except psycopg2.DatabaseError as e:
  print('Failed to connect to Postgres DB: {}'.format(e));


def get_classified_set():
  SQL = "SELECT user_id, feature_vector, classification FROM classified_ds ORDER BY user_id ASC;"
  cursor.execute(SQL);
  entries = cursor.fetchall()
  data_set = []
  for entry in entries: 
    formated_entry = ([float(feature) for feature in entry[1]],entry[2])
    data_set.append(formated_entry)
  return data_set
 
def store_classified_set(data_set):
  for entry in data_set:
    SQL = "INSERT INTO classified_ds (user_id, user_name, feature_vector, classification) VALUES(%s, %s, %s, %s) ON CONFLICT (user_id) DO NOTHING;"
    cursor.execute(SQL,(entry[0],entry[1],entry[2],entry[3]))
  try:
    connection.commit()
  except Exception as e:
    print('Failed to save entry with error: {}'.format(e))

def retrieve_list_of_news_sites():
  cursor.execute("SELECT related_account_name,related_account_id, url FROM news_sites;")
  entries = cursor.fetchall()
  return [{'screen_name':entry[0], 'id': entry[1], 'url': entry[2]} for entry in entries]

def store_news_site(entries):
  SQL = "INSERT INTO news_sites (related_account_name, related_account_id, url) VALUES (%s,%s,%s);"
  for entry in entries:
    # print(entry)
    cursor.execute(SQL, entry)
  connection.commit()

def close_connection():
  if connection:
    connection.commit()
  cursor.close()
  connection.close()

