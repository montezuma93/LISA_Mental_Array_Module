from Relation import *
import csv
import requests
import json
import ccobra
import numpy
import math

start_simulation_url = 'http://localhost:5000/start_simulation'

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def calculate_angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def cast_relation_to_spatial(relation):
    dictionary = {'West': 'Left', 'East':'Right'}
    return dictionary.get(relation,'Relation Not Found')

def get_relation(spatial_array, object1, object2, use_cardinal_relation):
    vector_to_relation_mapping_dict = {'North': (1,0), 'South': (-1,0),'West': (0,1), 'East': (0,-1), 'NorthEast': (1,-1), 'NorthWest': (1,1), 'SouthEast': (-1,-1), 'SouthWest': (-1,1)}
    spatial_array_as_matrix = numpy.matrix(spatial_array)
    object1_itemindex = numpy.where(spatial_array_as_matrix==object1)
    object2_itemindex = numpy.where(spatial_array_as_matrix==object2)
    object1_index_y = object1_itemindex[0]
    object1_index_x = object1_itemindex[1]
    object2_index_y = object2_itemindex[0]
    object2_index_x = object2_itemindex[1]
    vector_x = object2_index_x - object1_index_x
    vector_y = object2_index_y - object1_index_y
    best_fit_relation = ""
    closest_angle = 360
    for relation, relation_angle in vector_to_relation_mapping_dict.items():
        angle = calculate_angle((vector_y, vector_x), relation_angle)
        dif = abs(angle-0)
        if dif < closest_angle:
            closest_angle = dif
            best_fit_relation = relation
    relation_to_return = best_fit_relation
    if use_cardinal_relation == False:
        relation_to_return = cast_relation_to_spatial(best_fit_relation)
    return relation_to_return


def run(item):
    tasks = item.task
    choices = item.choices
    propositions = []
    for propositions_to_save in tasks:
        propositions.append(
        {
            "relationName": propositions_to_save[0],
            "objectName1": propositions_to_save[1],
            "objectName2": propositions_to_save[2]
        })
        
    propositions_to_save_data = {
        "propositions": propositions,
        "size": "21",
        "unmarkedDistance": "4",
        "markedDistance": "4",
        "standardDeviation": "0.0",
        "amountOfFiringEvents": "10"
    }

    propositions_to_save_json = json.dumps(propositions_to_save_data)

    response_of_call = requests.post(start_simulation_url, data=propositions_to_save_json, headers={"Content-Type": "application/json", "Accept": "application/json"})
    response_in_json = response_of_call.json()
    spatial_array = response_in_json['spatial_array']

    use_cardinal_relation = True
    sumlation_thinks_all_facts_correct = True
    for choice in enumerate(choices[0]):
        relation = choice[1][0]
        object1 = choice[1][1]
        object2 = choice[1][2]
        if relation == "Left" or relation == "Right":
            use_cardinal_relation = False   
        simulation_relation = get_relation(spatial_array, object1, object2, use_cardinal_relation)
        if relation != simulation_relation:
            sumlation_thinks_all_facts_correct = False
    return sumlation_thinks_all_facts_correct
   

"""
Returns all cardinal direction (inclusive inter cardinal directions) (marked and unmarked distance is the same) (no random)
"""
class Model2(ccobra.CCobraModel):

    def __init__(self, name='Model2'):
        super(Model2, self).__init__(name, ['spatial-relational'], ['verify', 'single_choice'])

    def predict(self, item, **kwargs):
        return run(item)