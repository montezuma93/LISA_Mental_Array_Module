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
        self.objects = []
        self.spatial_array = numpy.empty([self.SIZE, self.SIZE], dtype=object) 
        
    def insert_proposition(self, relation, object1, object2):
        if self.objects.__contains__(object1) and not self.objects.__contains__(object2):
            self.objects.append(object2)
            self.add_object_by_lxr_units(relation, object1, object2, False)
        elif self.objects.__contains__(object2) and not self.objects.__contains__(object1):
            self.objects.append(object1)
            self.add_object_by_lxr_units(relation, object2, object1, True)
        else:
            self.objects.append(object1)
            self.objects.append(object2)
            self.fill_spatial_array_with_new_object(relation, object1, True)
            self.fill_spatial_array_with_new_object(relation, object2, False)

    def add_object_by_lxr_units(self, relation, reference_object, object_to_add, is_agent):
        itemindex = numpy.where(self.spatial_array==reference_object)
        new_index_y = itemindex[0][0]
        new_index_x = itemindex[1][0]
        if is_agent:
            new_index_y = self.find_min_and_max_limit(new_index_y, relation.agent_y_lxr_units)
            new_index_x = self.find_min_and_max_limit(new_index_x , relation.agent_x_lxr_units)
        else:
            new_index_y = self.find_min_and_max_limit(new_index_y, relation.referent_y_lxr_units)
            new_index_x = self.find_min_and_max_limit(new_index_x, relation.referent_x_lxr_units)
        next_item = self.spatial_array.item((new_index_y, new_index_x))
        print(next_item)
        if next_item is not None:
            self.add_object_to_next_empty_cell(new_index_y, new_index_x, relation, object_to_add, is_agent)
        else:
            self.spatial_array.itemset((new_index_y, new_index_x), object_to_add)

    def add_object_to_next_empty_cell(self, index_x, index_y, relation, object_to_add, is_agent):
        new_index_y = index_y
        new_index_x = index_x
        x_direction = 0
        y_direction = 0
        if is_agent:
            if relation.agent_y_lxr_units > 0:
                y_direction = 1
            elif relation.agent_y_lxr_units == 0:
                y_direction = 0
            else:
                y_direction = -1
            if relation.agent_x_lxr_units > 0:
                x_direction = 1
            elif relation.agent_x_lxr_units == 0:
                x_direction = 0
            else:
                x_direction = -1
        else:
            if relation.referent_y_lxr_units > 0:
                y_direction = 1
            elif relation.referent_y_lxr_units == 0:
                y_direction = 0
            else:
                y_direction = -1
            if relation.referent_x_lxr_units > 0:
                x_direction = 1
            elif relation.referent_x_lxr_units == 0:
                x_direction = 0
            else:
                x_direction = -1

        next_item = ""
        while next_item is not None:
            next_new_index_y = self.find_min_and_max_limit(new_index_y, y_direction)
            next_new_index_x = self.find_min_and_max_limit(new_index_x , x_direction)
            if next_new_index_x == new_index_x and next_new_index_y == new_index_y:
                print("No empty cell found")
                return
            new_index_y = next_new_index_y
            new_index_x = next_new_index_x
            next_item = self.spatial_array.item((new_index_y, new_index_x))
        self.spatial_array.itemset((new_index_y, new_index_x), object_to_add)


    def find_min_and_max_limit(self, index, index_to_add):
        if index + index_to_add >= self.SIZE:
            return self.SIZE -1
        elif index + index_to_add < 0:
            return 0
        else:
            return index + index_to_add
        

    def fill_spatial_array_with_new_object(self, relation, object_to_map, is_agent):
        print(type(relation).__name__)
        if type(relation).__name__ == Relation.North.name:
            location = self.calculate_probability(self.HIGH_AGENT_MEAN, is_agent)
            self.spatial_array.itemset((self.SIZE-1 - location,4),object_to_map)
        elif type(relation).__name__ == Relation.South.name:
            location = self.calculate_probability(self.LOW_AGENT_MEAN, is_agent)
            self.spatial_array[self.SIZE-1 - location][4] = object_to_map     
        elif type(relation).__name__ == Relation.West.name:  
            location = self.calculate_probability(self.LOW_AGENT_MEAN, is_agent)
            self.spatial_array[4][location] = object_to_map
        elif type(relation).__name__ == Relation.East.name:  
            location = self.calculate_probability(self.HIGH_AGENT_MEAN, is_agent)
            self.spatial_array[4][location] = object_to_map 
        elif type(relation).__name__ == Relation.NorthWest.name: 
            location = self.calculate_probability(self.HIGH_AGENT_MEAN, is_agent)
            self.spatial_array[self.SIZE-1 - location][self.SIZE-1 - location] = object_to_map 
        elif type(relation).__name__ == Relation.NorthEast.name: 
            location = self.calculate_probability(self.HIGH_AGENT_MEAN, is_agent)
            self.spatial_array[self.SIZE-1 - location][location] = object_to_map 
        elif type(relation).__name__ == Relation.SouthWest.name:  
            location = self.calculate_probability(self.LOW_AGENT_MEAN, is_agent)
            self.spatial_array[self.SIZE-1 - location][location] = object_to_map 
        elif type(relation).__name__ == Relation.SouthEast.name: 
            location = self.calculate_probability(self.LOW_AGENT_MEAN, is_agent)
            self.spatial_array[self.SIZE-1 - location][self.SIZE-1 - location] = object_to_map 
        else:
            print("UNKNONW_RELATION")

    def calculate_probability(self, agent_mean, is_agent):
        if is_agent:
            x = numpy.random.normal(agent_mean, self.STANDARD_VARIATION, self.AMOUNT_OF_FIRING_EVENTS)
            mean = numpy.mean(x)
            return int(round(mean))
        else:
            x = numpy.random.normal(self.REFERENT_MEAN, self.STANDARD_VARIATION, self.AMOUNT_OF_FIRING_EVENTS)
            mean = numpy.mean(x)
            return int(round(mean))


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





