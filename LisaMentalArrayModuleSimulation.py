from MentalArrayModule import MentalArrayModule
from Relation import *
import json
from flask import Flask, request, json, jsonify
from flask_restplus import Resource, Api, reqparse, Swagger,fields

app = Flask(__name__)
class LisaMentalArrayModuleSimulation(Resource):

    def __init__(self, app):
        self.mental_array_module = MentalArrayModule()
        self.mental_array_module.start(9, 2, 1)
    '''
    def reset_simulation(self):
        self.mental_array_module.reset_simulation()
    '''
    def insert_proposition(self, relation, object1, object2):
        self.mental_array_module.insert_proposition(relation, object1, object2)


@app.route("/start_simulation", methods=['POST'])
def start_simulation():     
    req_data = request.get_json()
    propositions = req_data['propositions']
    for proposition in propositions:
        relation = cast_relation(proposition['relationName'])
        object1 = proposition['objectName1']
        object2 = proposition['objectName2']
        lisa_mental_array_module_simulation.insert_proposition(relation, object1, object2)
        lisa_mental_array_module_simulation.mental_array_module.print_all()

    return 'relation finished'
'''
@app.route("/update_settings", methods=['POST'])
def update_settings():     
    req_data = request.get_json()
    base_activation_decay = req_data['base_activation_decay']
    fraction_of_activation = req_data['fraction_of_activation']
    initial_activation_value = req_data['initial_activation_value']
    noise = req_data['noise']
    dynamic_firing_threshold = req_data['dynamic_firing_threshold']
    firing_threshold = req_data['firing_threshold']
    noise_on = req_data['noise_on']
    spread_full_activation = req_data['spread_full_activation']
    use_only_complete_fragments = req_data['use_only_complete_fragments']

    lisa_mental_array_module_simulation.update_settings(base_activation_decay, fraction_of_activation, initial_activation_value, noise,
     dynamic_firing_threshold, firing_threshold, noise_on, spread_full_activation, use_only_complete_fragments)
    return 'settings_updated'

@app.route("/reset_simulation", methods=['POST'])
def reset_simulation():     
    lisa_mental_array_module_simulation.reset_simulation()
    return 'settings_updated'
'''
def cast_relation(relation):
    dictionary = {'North':North(), 'South':South(), 'West':West(), 'East': East(),
       'NorthEast': NorthEast(), 'NorthWest': NorthWest(), 'SouthEast': SouthEast(), 'SouthWest': SouthWest()}
    return dictionary.get(relation,'Relation Not Found')

lisa_mental_array_module_simulation = LisaMentalArrayModuleSimulation(app)

if __name__ == '__main__':
    app.run()
