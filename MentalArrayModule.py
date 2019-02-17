import numpy
from scipy.stats import norm
import logging
from Relation import *

class MentalArrayModule:

    """
    Initialize a new mental array module
    """
    def __init__(self):
        self.logger = logging.getLogger('MentalArrayModule')
        self.logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        self.logger.addHandler(stream_handler)

    """
    Initialize a new mental array module

    Parameters
    ----------
    param1 : int
        size of the grid of the spatial array (should be odd to have a certain mid)
    
    param2 : int
        distance of the agent to the referent object if the relation is unmarked (-> see in Relation.py, which relation is marked or unmarked)
   
    param3 : int
        distance of the agent to the referent object if the relation is marked (-> see in Relation.py, which relation is marked or unmarked)

    param4 : float
        standard deviation which is used to calculate the cell where to save object, which will get decided by a gaussian distribution (choose 0.0 to remove random)

    param5 : int
        amount of times, the gaussian distribution will choose a cell where to set an object (the lower the number the more random)
    """   
    def start(self, size, unmarked_distance, marked_distance, standard_deviation, amount_of_firing_events):
        self.size = size
        self.unmarked_distance = unmarked_distance
        self.marked_distance = marked_distance
        self.standard_deviation = standard_deviation
        self.amount_of_firing_times = amount_of_firing_events

        self.objects = []
        self.spatial_array = numpy.empty([self.size, self.size], dtype=object)

    """
    Insert a new proposition. If one of the two objects already in the spatial array. Insert the other object based on the
    already saved object. If the insertion was successful the added object will be added to the list, containing all object which
    are in the spatial array

    Parameters
    ----------
    param1 : Relation
        the relation which should get placed in the spatial array, this relation explains the relation of object1 to object2
    
    param2 : String
        string representation of the first object
    
    param3 : String
        string representation of the second object
    """ 
    def insert_proposition(self, relation, object1, object2):
        self.logger.info('Insert proposition with relation: %s, object1: %s, object2: %s', type(relation).__name__, object1, object2)
        if self.objects.__contains__(object1) and not self.objects.__contains__(object2):
            object_was_inserted = self.add_object_by_reference_object_and_lxr_units(relation, object1, object2, False)
            if object_was_inserted:
                self.objects.append(object2)
        elif self.objects.__contains__(object2) and not self.objects.__contains__(object1):
            object_was_inserted = self.add_object_by_reference_object_and_lxr_units(relation, object2, object1, True)
            if object_was_inserted:
                self.objects.append(object1)
        else:
            self.objects.append(object1)
            self.objects.append(object2)
            self.add_new_object_to_spatial_array(relation, object1, True)
            self.add_new_object_to_spatial_array(relation, object2, False)

    """
    Insert an object to the spatial array, based on a referent object. If it can be added in the calculated cell, returns true.
    If the calculated cell is outside of the grid, it returns false
    If the calculated cell is blocked by another object, calculate next empty cell by anther method

    Parameters
    ----------
    param1 : Relation
        the relation which should get placed in the spatial array, this relation explains the relation of object1 to object2.
        the relation is need to know where the relation is marked or not and to get lxr units for x and y direction
    
    param2 : String
        string representation of the reference object
    
    param3 : String
        string representation of the object to add
    
    param4 : boolean
        true if the object to add is the agent of the relation, false if it is the referent

    Returns
    --------
    boolean
        true if the object was added, false if it wasn't possible to add it
    """ 
    def add_object_by_reference_object_and_lxr_units(self, relation, reference_object, object_to_add, is_agent):
        reference_object_itemindex = numpy.where(self.spatial_array==reference_object)
        lxr_units_in_x_direction = 0
        lxr_units_in_y_direction = 0
        if is_agent:
            lxr_units_in_x_direction = self.map_direction_to_lxr_units(relation.agent_x_direction, relation.is_marked)
            lxr_units_in_y_direction = self.map_direction_to_lxr_units(relation.agent_y_direction, relation.is_marked)
        else:
            lxr_units_in_x_direction = self.map_direction_to_lxr_units(relation.referent_x_direction, relation.is_marked)
            lxr_units_in_y_direction = self.map_direction_to_lxr_units(relation.referent_y_direction, relation.is_marked)
        calculated_index_y = self.calculate_new_index(reference_object_itemindex[0][0], lxr_units_in_y_direction)
        calculated_index_x = self.calculate_new_index(reference_object_itemindex[1][0] , lxr_units_in_x_direction)
        if calculated_index_y == -1 or calculated_index_x == -1:
            self.logger.info("No space found for the object: %s", object_to_add)
            return False
        calculated_item = self.spatial_array.item((calculated_index_y, calculated_index_x))
        if calculated_item is not None:
            object_was_inserted = self.add_object_to_next_empty_cell(calculated_index_x, calculated_index_y, lxr_units_in_x_direction, lxr_units_in_y_direction, object_to_add)
            return object_was_inserted
        else:
            self.logger.info("Added object: %s in spatial array in cell [%s] [%s] ", object_to_add, calculated_index_y, calculated_index_x)
            self.spatial_array.itemset((calculated_index_y, calculated_index_x), object_to_add)
            return True

    """
    Map lxrDirection to units based on the marked or unmarked distance

    Parameters
    ----------
    param1 : LxrDirection
        lxr_direction describes if plus, zero or minus in x and y direction
    
    param2 : boolean
        true if the relation is marked, false if it is unmarked
    
    Returns
    --------
    int
        amount in the direction
    """ 
    def map_direction_to_lxr_units(self, direction, is_marked):
        if direction == Direction.Plus:
            if is_marked:
                return self.marked_distance
            else:
                return self.unmarked_distance
        elif direction == Direction.Minus:
            if is_marked:
                return self.marked_distance * -1
            else:
                return self.unmarked_distance * -1
        else:
            return 0

    """
    Calculate the next index based on index plus direction. Checks whether the new index is outside of the grid
    
    Parameters
    ----------
    param1 : int
        index from which the lxr units get added
    
    param2 : int
        lxr units to add
    
    Returns
    --------
    int
        returns the new index, returns -1 if it was outside of the grid
    """ 
    def calculate_new_index(self, index, index_to_add):
        if index + index_to_add >= self.size or index + index_to_add < 0:
            return -1
        else:
            return index + index_to_add

    """
    Look for next empty cell to add object. This method was called cause cell was already blocked by another object

    Parameters
    ----------
    param1 : int
        x value of the cell where the object should got added, but was blocked
    
    param2 : int
        y value of the cell where the object should got added, but was blocked
    
    param1 : int
        x direction in which this method should look for an empty cell to add the object
    
    param2 : int
        y direction in which this method should look for an empty cell to add the object
    
    param2 : String
        string representation of the name of the object that should get added
    
    Returns
    --------
    boolean
        true if the object was added, false if the object wasn't able to get added
    """ 
    def add_object_to_next_empty_cell(self, index_x, index_y, direction_x, direction_y, object_to_add):
        normalized_x_direction = self.normalize_lxr_units(direction_x)
        normalized_y_direction = self.normalize_lxr_units(direction_y)
        calculated_item = ""
        while calculated_item is not None:
            index_y = self.calculate_new_index(index_y, normalized_y_direction)
            index_x = self.calculate_new_index(index_x , normalized_x_direction)
            if index_y == -1 or index_x == -1:
                self.logger.info("No space found for the object: %s. Not possible to add it to spatial array", object_to_add)
                return False
            calculated_item = self.spatial_array.item((index_y, index_x))
        self.spatial_array.itemset((index_y, index_x), object_to_add)
        self.logger.info("Object: %s was added in cell [%s][%s] in the spatial array", object_to_add, index_y, index_x)
        return True

    """
    Normalize lxr units in range from -1 to 1. In order to find next empty cell

    Parameters
    ----------
    param1 : int
        lxr unit value which should get normalized
    
    Returns
    --------
    int
        normalized lxr unit (-1, 0 or 1)
    """ 
    def normalize_lxr_units(self, direction):
        if direction > 0:
            return 1
        elif direction < 0:
            return -1
        else:
            return 0

    """
    Fill a new object to the grid, if none of the objects of an relation were already in the grid
    If it is already blocked, random again
    
    Parameters
    ----------
    param1 : Relation
        relation of the object that should get added
    
    param2 : String
        string representation of the objects name
     
    param3 : boolean
        true if the object to add is the agent of the relation, false if it is the referent
    
    """
    def add_new_object_to_spatial_array(self, relation, object_to_add, is_agent):
        object_was_added = False
        while not object_was_added:
            location = self.calculate_location_for_new_object(relation, is_agent)
            index_x = 0
            index_y = 0
            if type(relation).__name__ == Relation.North.name or type(relation).__name__ == Relation.South.name:
                index_x = int((self.size - 1)/2)
                index_y = location
            elif (type(relation).__name__ == Relation.West.name or type(relation).__name__ == Relation.East.name 
             or type(relation).__name__ == Relation.Left.name or type(relation).__name__ == Relation.Right.name):
                index_x = location
                index_y = int((self.size - 1)/2)
            elif type(relation).__name__ == Relation.NorthWest.name or type(relation).__name__ == Relation.SouthEast.name:
                index_x = location
                index_y = location
            elif type(relation).__name__ == Relation.NorthEast.name:
                index_x = self.size-1 - location
                index_y = location
            elif type(relation).__name__ == Relation.SouthWest.name:
                index_x = location
                index_y = self.size-1 - location
            object_was_added = self.add_object_in_empty_cell(index_x, index_y, object_to_add)

    """
    Add object in spatial array, if the cell is empty
    
    Parameters
    ----------
    param1 : int
        index_x of the spatial array, where the object should get added
    
    param1 : int
        index_y of the spatial array, where the object should get added
     
    param3 : String
        the object, that should be added
    
    Returns
    --------
    boolean
        true if the object was added, false if the object wasn't able to get added
    
    """
    def add_object_in_empty_cell(self, index_x, index_y, object_to_add):
        if self.spatial_array[index_y][index_x] == None:
            self.spatial_array[index_y][index_x] = object_to_add
            self.logger.info("Object: %s was added in cell [%s][%s] in the spatial array", object_to_add, index_y, index_x)
            return True
        else:
            return False

    """
    Calculate the location of an new object based on its relation or if the object is agent of the relation
    
    Parameters
    ----------
    param1 : Relation
        relation of the object that should get added

    param2 : boolean
        true if the object to add is the agent of the relation, false if it is the referent
  
    Returns
    --------
    int
        returns location where to object should get added
    """   
    def calculate_location_for_new_object(self, relation, is_agent):
        referent_mean = int((self.size -1) /2)
        if is_agent:
            if relation.mean == Mean.High and relation.is_marked:
                return self.calculate_location_with_gaussian_distribution(referent_mean + self.marked_distance)
            elif relation.mean == Mean.Low and relation.is_marked:
                return self.calculate_location_with_gaussian_distribution(referent_mean - self.marked_distance)
            elif relation.mean == Mean.High and not relation.is_marked:
                return self.calculate_location_with_gaussian_distribution(referent_mean + self.unmarked_distance)
            else:
                return self.calculate_location_with_gaussian_distribution(referent_mean - self.unmarked_distance)
        else:
            return self.calculate_location_with_gaussian_distribution(referent_mean)

    """
    Calculate the cell where to put the element which should get added
    Calculation is based on gaussian distribution, realized by the standard_deviation, which got set while initialization and
    the mean which got calculated by the size of the grid as well as the distance which an agent object has to its referent.
    This distance is also set while initialization.
    The cell is also calculated by an defined amount of firing events. Which will calculate a number each firing time and calculate its
    average. Which means, the less calls the random the cell where the element get placed.

    Parameters
    ----------
    param1 : int
        the cell which represents the mean of the gaussian distribution. The object should be placed close to that mean.

    Returns
    --------
    int
        the cell where the object get placed
    """ 
    def calculate_location_with_gaussian_distribution(self, mean):
        x = numpy.random.normal(mean, self.standard_deviation, self.amount_of_firing_times)
        mean = numpy.mean(x)
        return int(round(mean))

    """
    Get the spatial array as object
    
    Returns
    --------
    Object
        returns an object representation of the spatial array(can be turned into json later)
    """ 
    def get_spatial_array(self):
        spatial_array = self.spatial_array.tolist()
        return {
            "spatial_array": spatial_array
        }
