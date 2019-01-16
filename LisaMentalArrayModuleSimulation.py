from MentalArrayModule import MentalArrayModule
from Relation import North, West, South, East, NorthEast, NorthWest, SouthEast, SouthWest, Left, Right
import json
from flask import Flask, request, json
from flask_restplus import Resource, Api, reqparse, Swagger,fields

app = Flask(__name__)
class LisaMentalArrayModuleSimulation(Resource):

    def __init__(self, app):
        self.mental_array_module = MentalArrayModule()

    def start(self, size, unmarked_distance, marked_distance, standard_deviation, amount_of_firing_events):
        self.mental_array_module.start(size, unmarked_distance, marked_distance, standard_deviation, amount_of_firing_events)

    def get_spatial_array(self):
        return json.dumps(self.mental_array_module.get_spatial_array())

    def insert_proposition(self, relation, object1, object2):
        self.mental_array_module.insert_proposition(relation, object1, object2)

@app.route("/start_simulation", methods=['POST'])
def start_simulation():     
    req_data = request.get_json()
    size = int(req_data['size'])
    unmarked_distance = int(req_data['unmarkedDistance'])
    marked_distance = int(req_data['markedDistance'])
    standard_deviation = float(req_data['standardDeviation'])
    amount_of_firing_events = int(req_data['amountOfFiringEvents'])
    lisa_mental_array_module_simulation.start(size, unmarked_distance, marked_distance, standard_deviation, amount_of_firing_events)
    propositions = req_data['propositions']
    for proposition in propositions:
        relation = cast_relation(proposition['relationName'])
        object1 = proposition['objectName1']
        object2 = proposition['objectName2']
        lisa_mental_array_module_simulation.insert_proposition(relation, object1, object2)
    return lisa_mental_array_module_simulation.get_spatial_array()

def cast_relation(relation):
    dictionary = {'North':North(), 'South':South(), 'West':West(), 'East': East(),
       'NorthEast': NorthEast(), 'NorthWest': NorthWest(), 'SouthEast': SouthEast(), 'SouthWest': SouthWest(),
       'Left': Left(), 'Right': Right()}
    return dictionary.get(relation,'Relation Not Found')

lisa_mental_array_module_simulation = LisaMentalArrayModuleSimulation(app)

if __name__ == '__main__':
    app.run()
