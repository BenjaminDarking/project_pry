import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))
from classifier.knn_classifier import knn_classifier
from classifier.model import inference
from filters.verified_filter import unverified_and_unprotected_user_filter
from filters.run_filters import get_chosen_filters, get_training_set_id, run_filters_on_user
from db.postgresql_storage import get_classified_set


#----------------------------------------------------------------
#                     DB interactions
#---------------------------------------------------------------- 

def get_classified_set_from_db(): #From Postgres
  classified_list = get_classified_set()
  return [e for e in classified_list if e != 'null'] 


#---------------------------------------------------------------
#                   User Classification
#---------------------------------------------------------------

def classify_vector(tested_vector, classifier):
  if classifier[0] == 'knn':
    classified_set = get_classified_set_from_db()
    classification = knn_classifier(classified_set,tested_vector,classifier[1])
    return (tested_vector, classification)
  else:
    data_set_id = classifier[1]
    classified_set = get_classified_set_from_db(data_set_id)
    classification, probablity = inference(classified_set,tested_vector)
    return (tested_vector, classification, probability)


def classify_user(user, filters, classifier):
  if unverified_and_unprotected_user_filter(user):
    tested_vector = run_filters_on_user(filters,user)
    classification_res = classify_vector(tested_vector,classifier)
    return classification_res
  else:
    return

def classify_users(users, filters, classifier=('knn',3)):
  f_tuples = get_chosen_filters(filters)
  if classifier[0] == 'model':
    testing_set_id = get_testing_set_id(f_tuples)
    classifier[1] = testing_set_id
 
  classified_users = [] 
  for user in users:
    classified_user = classify_user(user,f_tuples,classifier) 
    #print(classified_user)
    if classified_user:
      classified_users.append(classified_user)
  print(classified_users)
  return classified_users

#--------------------------------------------------------------------
#                         Data_set Prep
#--------------------------------------------------------------------

def run_filters_on_users(users, filters,bots=True):
  f_tuples = get_chosen_filters(filters)
  data_set = []
  for user in users:
    if unverified_and_unprotected_user_filter(user):
      tested_vector = run_filters_on_user(f_tuples,user)
      data_entry = [user['id'],user['screen_name'],tested_vector,int(bots)]
      data_set.append(data_entry)
  #print(data_set)
  return data_set


