import numpy
import sys
from scipy.stats import norm
from Relation import *
from pandas import *
class MentalArrayModule:

    SIZE = 9
    MARKED_RELATION_DISTANCE = 2
    UNMARKED_RELATION_DISTANCE = 2
    STANDARD_VARIATION = 0.5
    AMOUNT_OF_FIRING_EVENTS = 10

    def __init__(self, size, marked_relation_distance, un_marked_relation_distance):
        self.objects = []
        self.SIZE = size
        self.MARKED_RELATION_DISTANCE = marked_relation_distance
        self.UNMARKED_RELATION_DISTANCE = un_marked_relation_distance
        self.referent_mean = int((self.SIZE -1) /2)
        self.marked_high_agent_mean = self.referent_mean + self.MARKED_RELATION_DISTANCE
        self.unmarked_high_agent_mean = self.referent_mean + self.UNMARKED_RELATION_DISTANCE
        self.marked_low_agent_mean = self.referent_mean - self.MARKED_RELATION_DISTANCE
        self.unmarked_low_agent_mean = self.referent_mean - self.UNMARKED_RELATION_DISTANCE
        self.spatial_array = numpy.empty([self.SIZE, self.SIZE], dtype=object)
        
    def insert_proposition(self, relation, object1, object2):
        if self.objects.__contains__(object1) and not self.objects.__contains__(object2):
            object_was_inserted = self.add_object_by_lxr_units(relation, object1, object2, False)
            if object_was_inserted:
                self.objects.append(object2)
        elif self.objects.__contains__(object2) and not self.objects.__contains__(object1):
            object_was_inserted = self.add_object_by_lxr_units(relation, object2, object1, True)
            if object_was_inserted:
                self.objects.append(object1)
        else:
            self.objects.append(object1)
            self.objects.append(object2)
            self.fill_spatial_array_with_new_object(relation, object1, True)
            self.fill_spatial_array_with_new_object(relation, object2, False)

    def add_object_by_lxr_units(self, relation, reference_object, object_to_add, is_agent):
        reference_object_itemindex = numpy.where(self.spatial_array==reference_object)
        object_to_add_index_x = reference_object_itemindex[1][0]
        object_to_add_index_y = reference_object_itemindex[0][0]
        lxr_x_direction = 0
        lxr_y_direction = 0
        if is_agent:
            lxr_x_direction = self.get_lxr_units(relation.agent_x_lxr_units, relation.is_marked)
            lxr_y_direction = self.get_lxr_units(relation.agent_y_lxr_units, relation.is_marked)
            object_to_add_index_y = self.find_min_and_max_limit(reference_object_itemindex[0][0], lxr_y_direction)
            object_to_add_index_x = self.find_min_and_max_limit(reference_object_itemindex[1][0] , lxr_x_direction)
        else:
            lxr_x_direction = self.get_lxr_units(relation.referent_x_lxr_units, relation.is_marked)
            lxr_y_direction = self.get_lxr_units(relation.referent_y_lxr_units, relation.is_marked)
            object_to_add_index_y = self.find_min_and_max_limit(reference_object_itemindex[0][0], lxr_y_direction)
            object_to_add_index_x = self.find_min_and_max_limit(reference_object_itemindex[1][0], lxr_x_direction)
        if object_to_add_index_y == -1 or object_to_add_index_x == -1:
            print("no space found")
            return False
        next_item = self.spatial_array.item((object_to_add_index_y, object_to_add_index_x))
        if next_item is not None:
            object_was_inserted = self.add_object_to_next_empty_cell(object_to_add_index_x, object_to_add_index_y, lxr_x_direction, lxr_y_direction, object_to_add)
            return object_was_inserted
        else:
            self.spatial_array.itemset((object_to_add_index_y, object_to_add_index_x), object_to_add)
            return True

    def get_lxr_units(self, lxr_direction, is_marked):
        if lxr_direction == LxrDirection.Plus:
            if is_marked:
                return self.MARKED_RELATION_DISTANCE
            else:
                return self.UNMARKED_RELATION_DISTANCE
        elif lxr_direction == LxrDirection.Minus:
            if is_marked:
                return self.MARKED_RELATION_DISTANCE * -1
            else:
                return self.UNMARKED_RELATION_DISTANCE * -1
        else:
            return 0


    def add_object_to_next_empty_cell(self, index_x, index_y, direction_x, direction_y, object_to_add):
        new_index_y = index_y
        new_index_x = index_x
        normalized_x_direction = self.normalize_lxr_units(direction_x)
        normalized_y_direction = self.normalize_lxr_units(direction_y)

        next_item = ""
        while next_item is not None:
            new_index_y = self.find_min_and_max_limit(new_index_y, normalized_y_direction)
            new_index_x = self.find_min_and_max_limit(new_index_x , normalized_x_direction)
            if new_index_y == -1 or new_index_x == -1:
                print("No empty cell found")
                return False
            next_item = self.spatial_array.item((new_index_y, new_index_x))
        self.spatial_array.itemset((new_index_y, new_index_x), object_to_add)
        return True

    def normalize_lxr_units(self, direction):
        if direction > 0:
            return 1
        elif direction < 0:
            return -1
        else:
            return 0

    def find_min_and_max_limit(self, index, index_to_add):
        if index + index_to_add >= self.SIZE or index + index_to_add < 0:
            return -1
        else:
            return index + index_to_add

    def fill_spatial_array_with_new_object(self, relation, object_to_map, is_agent):
        location = self.calculate_location_for_new_object(relation, is_agent)
        if type(relation).__name__ == Relation.North.name or type(relation).__name__ == Relation.South.name:
            self.spatial_array.itemset((location, int((self.SIZE - 1)/2)), object_to_map) 
        elif type(relation).__name__ == Relation.West.name or type(relation).__name__ == Relation.East.name:  
            self.spatial_array.itemset((int((self.SIZE -1)/2), location), object_to_map)
        elif type(relation).__name__ == Relation.NorthWest.name or type(relation).__name__ == Relation.SouthEast.name: 
            self.spatial_array[location][location] = object_to_map 
        elif type(relation).__name__ == Relation.NorthEast.name: 
            self.spatial_array[location][self.SIZE-1 - location] = object_to_map 
        elif type(relation).__name__ == Relation.SouthWest.name:  
            self.spatial_array[self.SIZE-1 - location][location] = object_to_map 
        else:
            print("UNKNONW_RELATION")

    def calculate_location_for_new_object(self, relation, is_agent):
        if is_agent:
            if relation.mean == Mean.High and relation.is_marked:
                return self.calculate_probability(self.marked_high_agent_mean)
            elif relation.mean == Mean.Low and relation.is_marked:
                return self.calculate_probability(self.marked_low_agent_mean)
            elif relation.mean == Mean.High and not relation.is_marked:
                return self.calculate_probability(self.unmarked_high_agent_mean)
            else:
                return self.calculate_probability(self.unmarked_low_agent_mean)
        else:
            return self.calculate_probability(self.referent_mean)

    def calculate_probability(self, mean):
        x = numpy.random.normal(mean, self.STANDARD_VARIATION, self.AMOUNT_OF_FIRING_EVENTS)
        mean = numpy.mean(x)
        return int(round(mean))


    def print_all(self):
        print(DataFrame(self.spatial_array))

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
    is_running = True
    args = sys.argv[1:]
    if len(args) < 3 or int(args[0]) % 2 == 0:
        print("You need to enter an odd number as param for the size of the MAM as well as number for marked and unmarked relation distance")
        is_running = False
    
    mam = MentalArrayModule(int(args[0]), int(args[1]), int(args[2]))
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





