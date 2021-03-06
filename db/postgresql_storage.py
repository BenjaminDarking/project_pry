import psycopg2
import os
import sys
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))
import credentials


PGHOST=os.environ.get('PGHOST')
PGDATABASE=os.environ.get('PGDATABASE')
PGUSER=os.environ.get('PGUSER')
PGPASSWORD=os.environ.get('PGPASSWORD')

connection_string = "host="+ PGHOST +" port="+ "5432" +" dbname="+ PGDATABASE +" user=" + PGUSER \
    +" password="+ PGPASSWORD
connection = psycopg2.connect(connection_string)
print("Connected!")

def test_connection():
  pass

def get_classified_set(set_id):
  print('get_classified_set: {}'.format(set_id))
  SQL = "SELECT classified_samples FROM data_set WHERE set_id=(%s);"
  cursor.execute(SQL,(set_id,))
  entries = cursor.fetchall()
  #print(entries)
  samples = []
  for entry in entries:
    ds = json.loads(entry[0])
    for sample in ds:
      print('get sample = {}'.format(sample))
      samples.append((sample[0],sample[1]))
  return samples

def create_classified_set_entry(samples,set_id):
  print('create classified set samples = {}'.format(samples))
  SQL = "INSERT INTO data_set (set_id, classified_samples) VALUES (%s, %s);"
  cursor.execute(SQL, (set_id, json.dumps(samples),))
  connection.commit()

def retrieve_list_of_news_sites():
  cursor.execute("SELECT related_account_name,related_account_id, url FROM news_sites;")
  entries = cursor.fetchall()
  return [{'screen_name':entry[0], 'id': entry[1], 'url': entry[2]} for entry in entries]

def create_news_site_entry(entries):
  SQL = "INSERT INTO news_sites (related_account_name, related_account_id, url) VALUES (%s,%s,%s);"
  for entry in entries:
    #print(entry)
    cursor.execute(SQL, entry)
  connection.commit()

try:
  cursor = connection.cursor()
  #test_connection()
except psycopg2.DatabaseError as e:
  print('Failed to connect to Postgres db {}'.format(e));
#finally:
#  if connection:
#    connection.commit()
#    cursor.close()
#    connection.close()
#

