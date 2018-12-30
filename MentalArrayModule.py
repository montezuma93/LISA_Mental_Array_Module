import numpy
from scipy.stats import norm
from Relation import *

class MentalArrayModule:

    SIZE = 9
    MARKED_RELATION_DISTANCE_FROM_AGENT_TO_REFERENT = 1
    MARKED_RELATION_DISTANCE_FROM_REFERENT_TO_AGENT = 1
    UNMARKED_RELATION_DISTANCE_FROM_AGENT_TO_REFERENT = 2
    UNMARKED_RELATION_DISTANCE_FROM_REFERENT_TO_AGENT = 2
    HIGH_AGENT_MEAN = 6
    LOW_AGENT_MEAN = 2
    REFERENT_MEAN  = 4
    STANDARD_VARIATION = 0.75
    AMOUNT_OF_FIRING_EVENTS = 10

    def __init__(self):
        self.objects = {}
        
    def insert_proposition(self, relation, object1, object2):
        if self.objects.__contains__(object1) and not self.objects.__contains__(object2):
            self.objects[object2] = numpy.zeros((self.SIZE, self.SIZE))
            self.fill_probability_map_by_lxr_units(relation, object1, object2, False)
        elif self.objects.__contains__(object2) and not self.objects.__contains__(object1):
            self.objects[object1] = numpy.zeros((self.SIZE, self.SIZE))
            self.fill_probability_map_by_lxr_units(relation, object2, object1, True)
        else:
            self.objects[object1] = numpy.zeros((self.SIZE, self.SIZE))
            self.objects[object2] = numpy.zeros((self.SIZE, self.SIZE))
            self.fill_probability_map_for_new_object(relation, object1, True)
            self.fill_probability_map_for_new_object(relation, object2, False)

    def fill_probability_map_by_lxr_units(self, relation, reference_object, object_to_add, is_agent):
        reference_object_probability_map = self.objects[reference_object]
        object_to_add_probability_map =  self.objects[object_to_add]
        print(object_to_add_probability_map)
        for j, row in enumerate(reference_object_probability_map):
            for i, value in enumerate(row):
                if is_agent:
                    object_to_add_probability_map.itemset((j,i), reference_object_probability_map.item((self.find_min_and_max_limit(j, relation.agent_y_lxr_units), self.find_min_and_max_limit(i , relation.agent_x_lxr_units))))
                else:
                    object_to_add_probability_map.itemset((j,i), reference_object_probability_map.item((self.find_min_and_max_limit(j, relation.referent_y_lxr_units), self.find_min_and_max_limit(i , relation.referent_x_lxr_units))))

    def find_min_and_max_limit(self, index, index_to_add):
        if index + index_to_add >= self.SIZE:
            return self.SIZE -1
        elif index + index_to_add < 0:
            return 0
        else:
            return index + index_to_add
        

    def fill_probability_map_for_new_object(self, relation, object_to_map, is_agent):
        print(type(relation).__name__)
        if type(relation).__name__ == Relation.North.name:
            for location in range(self.SIZE):
                self.objects[object_to_map][self.SIZE-1 - location][4] = self.calculate_probability(location, self.HIGH_AGENT_MEAN, is_agent)
        elif type(relation).__name__ == Relation.South.name:
            for location in range(self.SIZE):
                self.objects[object_to_map][self.SIZE-1 - location][4] = self.calculate_probability(location, self.LOW_AGENT_MEAN, is_agent)      
        elif type(relation).__name__ == Relation.West.name:  
            for location in range(self.SIZE):
                self.objects[object_to_map][4][location] = self.calculate_probability(location, self.LOW_AGENT_MEAN, is_agent)
        elif type(relation).__name__ == Relation.East.name:  
            for location in range(self.SIZE):
                self.objects[object_to_map][4][location] = self.calculate_probability(location, self.HIGH_AGENT_MEAN, is_agent)    
        elif type(relation).__name__ == Relation.NorthWest.name:  
            for location in range(self.SIZE):
                self.objects[object_to_map][self.SIZE-1 - location][self.SIZE-1 - location] = self.calculate_probability(location, self.HIGH_AGENT_MEAN, is_agent)
        elif type(relation).__name__ == Relation.NorthEast.name:  
            for location in range(self.SIZE):
                self.objects[object_to_map][self.SIZE-1 - location][location] = self.calculate_probability(location, self.HIGH_AGENT_MEAN, is_agent)
        elif type(relation).__name__ == Relation.SouthWest.name:  
            for location in range(self.SIZE):
                self.objects[object_to_map][self.SIZE-1 - location][location] = self.calculate_probability(location, self.LOW_AGENT_MEAN, is_agent)
        elif type(relation).__name__ == Relation.SouthEast.name: 
            for location in range(self.SIZE):
                self.objects[object_to_map][self.SIZE-1 - location][self.SIZE-1 - location] = self.calculate_probability(location, self.LOW_AGENT_MEAN, is_agent)
        else:
            print("UNKNONW_RELATION")

    def calculate_probability(self, location, agent_mean, is_agent):
        if is_agent:
            return round(norm.pdf(location, agent_mean, self.STANDARD_VARIATION),3)
        else:
            return round(norm.pdf(location, self.REFERENT_MEAN, self.STANDARD_VARIATION),3)


    def print_all(self):
        print(numpy.matrix(self.objects))

    def parse_input(self, input):
        arguments = input.split(" ")
        if len(arguments) != 3:
            print("Wrong amount of arguments")
            return []
        else:
            relation = self.cast_relation(arguments[0])
            arguments[0] = relation
            return arguments

    def cast_relation(self, relation):
        dictionary = {'North':North(), 'South':South(), 'West':West(), 'East': East(),
            'NorthEast': NorthEast(), 'NorthWest': NorthWest(), 
            'SouthEast': SouthEast(), 'SouthWest': SouthWest()}
        return dictionary.get(relation,'Relation Not Found')

if __name__ == '__main__':
    mam = MentalArrayModule()
    is_running = True
    while is_running:
        input_var = input("Enter something: ")
        print ("you entered " + input_var)
        if input_var == "Exit":
            is_running = False
            mam.print_all()
        else:
            arguments = mam.parse_input(input_var)
            if arguments is not None:
                mam.insert_proposition(arguments[0], arguments[1], arguments[2])





