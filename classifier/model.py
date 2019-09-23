import math

def apply_logistic_function(distance,k=1,L=1,x0=0):
  # Bigger distance -> smaller denominator -> f closer to 1; 
  # The probability of correct classification should be highest(1) when distance is smallest (0)
  f = 1 / (1 + math.exp(-k*(distance-x0)))
  probability = 1 - f
  return probability

def get_classification_probability(nearest_neighbours, classification):
  avg_squared_distance = sum([neighbour[1] for neighbour in nearest_neighbours])/len(nearest_neighbours)
  probability = apply_logistic_function(avg_squared_distance, x0 = len(nearest_neighbours[0][0])/2) #x0 = number of filters divided by half

def train_model():
  pass

def inference(classified_set, tested_set):
  pass
