import operator
import math
import random
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))
from db.postgresql_storage import get_classified_set


#---------------------------------------------------------------
#                 kNN Classifier Success Rate
#---------------------------------------------------------------

def get_knn_classifier_success_rate():
  classified_set = get_classified_set()
  no_of_tested_samples = int(len(classified_set)/4)
  tested_set_indices = random.sample(range(0,len(classified_set)),no_of_tested_samples)
  tested_set = []
  benchmark_set = []
  for index in range(len(classified_set)):
    sample = classified_set[index]
    tested_set.append(sample) if index in tested_set_indices else benchmark_set.append(sample)
  correct_classification = 0
  for sample in tested_set:
    classification = knn_classifier(benchmark_set,sample[0],3)
    if classification == sample[1]:
      correct_classification += 1
  return correct_classification/len(tested_set)



#---------------------------------------------------------------
#                       kNN Classifier
#--------------------------------------------------------------

#---------------------Utility functions-------------------------

def euclidean_distance(instance1, instance2, length):
  distance = 0
  for x in range(length):
	  distance += pow((instance1[x] - instance2[x]), 2)
  return distance

#--------------------------------------------------------------

def get_nearest_neighbours(classified_set, test_instance, k):
  distances = []
  length = len(test_instance)
  for x in range(len(classified_set)):
    dist = euclidean_distance(test_instance, classified_set[x][0], length)
    distances.append((classified_set[x], dist))
  distances.sort(key=operator.itemgetter(1))
  return distances[:k]

def decide_classification(nearest_neighbours):
  classification_avg = sum([neighbour[0][1] for neighbour in nearest_neighbours]) / len(nearest_neighbours)
  classification = int(classification_avg > 0.5) # More than half nearest neighbours are bots - return 1, otherwise 0
  return classification


def knn_classifier(data_set,test_instance,k):
  nearest_neighbours = get_nearest_neighbours(data_set, test_instance,k)
  classification = decide_classification(nearest_neighbours)
  return classification

#print('The success rate is: {}'.format(get_knn_classifier_success_rate()))
