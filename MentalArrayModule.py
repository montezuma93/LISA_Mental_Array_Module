import numpy
from scipy.stats import norm
from Relation import Relation

class MentalArrayModule:

    SIZE = 9
    MARKED_RELATION_DISTANCE = 2
    UNMARKED_RELATION_DISTANCE = 2
    HIGH_AGENT_MEAN = 6
    LOW_AGENT_MEAN = 2
    REFERENT_MEAN  = 4
    STANDARD_VARIATION = 0.75
    AMOUNT_OF_FIRING_EVENTS = 10

    def __init__(self):
        self.objects = {}
        
    def insert_proposition(self, relation, object1, object2):
        if self.objects.__contains__(object1):
            #TODO: go from there LxR units
            print(123)
        elif self.objects.__contains__(object1):
            print(123)
            #TODO: go from there LxR units
        else:
            print("here")
            self.objects[object1] = numpy.zeros((self.SIZE, self.SIZE))
            self.objects[object2] = numpy.zeros((self.SIZE, self.SIZE))
            self.fill_probability_map_for_object(relation, object1, True)
            self.fill_probability_map_for_object(relation, object2, False)


    def fill_probability_map_for_object(self, relation, object_to_map, is_agent):
        print(relation)
        if relation == Relation.North.name:
            for location in range(self.SIZE):
                self.objects[object_to_map][self.SIZE-1 - location][4] = self.calculate_probability(location, self.HIGH_AGENT_MEAN, is_agent)
        elif relation == Relation.South.name:
            for location in range(self.SIZE):
                self.objects[object_to_map][self.SIZE-1 - location][4] = self.calculate_probability(location, self.LOW_AGENT_MEAN, is_agent)      
        elif relation == Relation.West.name:  
            for location in range(self.SIZE):
                self.objects[object_to_map][4][location] = self.calculate_probability(location, self.HIGH_AGENT_MEAN, is_agent)
        elif relation == Relation.East.name:  
            for location in range(self.SIZE):
                self.objects[object_to_map][4][location] = self.calculate_probability(location, self.LOW_AGENT_MEAN, is_agent)    
        elif relation == Relation.NorthWest.name:  
            for location in range(self.SIZE):
                self.objects[object_to_map][self.SIZE-1 - location][self.SIZE-1 - location] = self.calculate_probability(location, self.HIGH_AGENT_MEAN, is_agent)
        elif relation == Relation.NorthEast.name:  
            for location in range(self.SIZE):
                self.objects[object_to_map][self.SIZE-1 - location][location] = self.calculate_probability(location, self.HIGH_AGENT_MEAN, is_agent)
        elif relation == Relation.SouthWest.name:  
            for location in range(self.SIZE):
                self.objects[object_to_map][self.SIZE-1 - location][location] = self.calculate_probability(location, self.LOW_AGENT_MEAN, is_agent)
        elif relation == Relation.SouthEast.name: 
            for location in range(self.SIZE):
                self.objects[object_to_map][self.SIZE-1 - location][self.SIZE-1 - location] = self.calculate_probability(location, self.LOW_AGENT_MEAN, is_agent)
        else:
            print("UNKNONW_RELATION")

    def calculate_probability(self, location, agent_mean, is_agent):
        print("heasdsadre")
        if is_agent:
            return round(norm.pdf(location, agent_mean, self.STANDARD_VARIATION),3)
        else:
            return round(norm.pdf(location, self.REFERENT_MEAN, self.STANDARD_VARIATION),3)

    def print_all(self):
        print(numpy.matrix(self.objects))

if __name__ == '__main__':
    mam = MentalArrayModule()
    mam.insert_proposition("South", "A", "B")
    mam.print_all()