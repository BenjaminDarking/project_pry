from random import randint, randrange, uniform
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))    
#from db.redis_cache import store_mock_data_set
from db.postgresql_storage import create_classified_set_entry

def create_random_sample(vector_length,indicies):
  #vector = [0] * vector_length
  v = []
  for i in indicies:
    v.append(randint(0,1) if i in [1,2] else uniform(0,1))

  #for i in [0,3,4,5]:
    #  vector[i] = uniform(0,1)

  #for i in [1,2]:
  #  vector[i] = randint(0,1)

  return v#vector

DEFAULT_SET_SIZE = 200

def create_test_set(set_id,size=DEFAULT_SET_SIZE):
  mock_data = []
  for i in range(size):
    vector = create_random_sample(6,[0,1,2,3,4,5])
    mock_data.append((vector, randint(0,1)))
  create_classified_set_entry(mock_data,set_id)

create_test_set(30030)
