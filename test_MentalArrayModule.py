import unittest
from unittest import mock
from mock import call, patch
from MentalArrayModule import MentalArrayModule
from Relation import *

class TestMentalArrayModule(unittest.TestCase):
    
    def test_mental_array_module_initialize_correctly(self):
        mental_array_module = self.create_mental_array_module()
        self.assertEqual(len(mental_array_module.objects), 0)

    @patch('MentalArrayModule.MentalArrayModule.fill_spatial_array_with_new_object')
    @patch('MentalArrayModule.MentalArrayModule.add_object_by_lxr_units')  
    def test_mental_array_module_should_call_correct_methods_for_new_proposition(self, mock_add_object_by_lxr_units, mock_fill_spatial_array_with_new_object):
        mental_array_module = MentalArrayModule()
        north_relation = North()
        west_relation = West()

        mental_array_module.insert_proposition(north_relation, "A", "B")
        mental_array_module.insert_proposition(north_relation, "B", "C")
        mental_array_module.insert_proposition(west_relation, "D", "C")
        mock_fill_spatial_array_with_new_object.assert_has_calls([call(north_relation, "A", True), call(north_relation, "B", False)]) 
        mock_add_object_by_lxr_units.assert_has_calls([call(north_relation, "B","C", False)])
        mock_add_object_by_lxr_units.assert_has_calls([call(west_relation, "C", "D", True)])     


    @patch('MentalArrayModule.MentalArrayModule.fill_spatial_array_with_new_object')
    def test_mental_array_module_should_call_correct_methods_for_multiple_propositions(self, mock_fill_spatial_array_with_new_object):
        mental_array_module = MentalArrayModule()
        north_relation = North()

        mental_array_module.insert_proposition(north_relation, "A", "B")
        mock_fill_spatial_array_with_new_object.assert_has_calls([call(north_relation, "A", True), call(north_relation, "B", False)])   

    def test_find_min_and_max_limit_with_size_9(self):
        mental_array_module = self.create_mental_array_module()

        self.assertEqual(mental_array_module.find_min_and_max_limit(1, 8), 8)
        self.assertEqual(mental_array_module.find_min_and_max_limit(1, 9), 8)
        self.assertEqual(mental_array_module.find_min_and_max_limit(3, -8), 0)
        self.assertEqual(mental_array_module.find_min_and_max_limit(1, -7), 0)

    def test_find_min_and_max_limit_with_size_12(self):
        mental_array_module = self.create_mental_array_module()
        mental_array_module.SIZE = 12

        self.assertEqual(mental_array_module.find_min_and_max_limit(1, 12), 11)
        self.assertEqual(mental_array_module.find_min_and_max_limit(0, 9), 9)
        self.assertEqual(mental_array_module.find_min_and_max_limit(3, -8), 0)
        self.assertEqual(mental_array_module.find_min_and_max_limit(9, -7), 2)

    def test_mental_array_module_correctly_insert_new_proposition(self):
        mental_array_module = self.create_mental_array_module()
        north_relation = North()

        mental_array_module.insert_proposition(north_relation, "A", "B")
        self.assertEqual(len(mental_array_module.objects), 2)
        self.assertEqual(mental_array_module.spatial_array[2][4], "A")
        self.assertEqual(mental_array_module.spatial_array[4][4], "B")

    def test_mental_array_module_correctly_insert_two_proposition(self):
        mental_array_module = self.create_mental_array_module()
        north_relation = North()
        
        mental_array_module.insert_proposition(north_relation, "A", "B")
        mental_array_module.insert_proposition(north_relation, "B", "C")

        self.assertEqual(len(mental_array_module.objects), 3)
        self.assertEqual(mental_array_module.spatial_array[2][4], "A")
        self.assertEqual(mental_array_module.spatial_array[4][4], "B")
        self.assertEqual(mental_array_module.spatial_array[6][4], "C")
    
    def test_mental_array_module_correctly_insert_multiple_proposition(self):
        mental_array_module = self.create_mental_array_module()
        north_relation = North()
        west_relation = West()

        mental_array_module.insert_proposition(north_relation, "A", "B")
        mental_array_module.insert_proposition(north_relation, "B", "C")
        mental_array_module.insert_proposition(west_relation, "D", "C")
        self.assertEqual(len(mental_array_module.objects), 4)
        self.assertEqual(mental_array_module.spatial_array[2][4], "A")
        self.assertEqual(mental_array_module.spatial_array[4][4], "B")
        self.assertEqual(mental_array_module.spatial_array[6][4], "C")
        self.assertEqual(mental_array_module.spatial_array[6][2], "D")
    
    def test_mental_array_module_correctly_insert_other_multiple_proposition(self):
        mental_array_module = self.create_mental_array_module()
        south_relation = South()
        west_relation = West()
        east_relation = East()

        mental_array_module.insert_proposition(south_relation, "A", "B")
        mental_array_module.insert_proposition(east_relation, "C", "B")
        mental_array_module.insert_proposition(west_relation, "D", "B")

        self.assertEqual(len(mental_array_module.objects), 4)
        self.assertEqual(mental_array_module.spatial_array[6][4], "A")
        self.assertEqual(mental_array_module.spatial_array[4][4], "B")
        self.assertEqual(mental_array_module.spatial_array[4][6], "C")
        self.assertEqual(mental_array_module.spatial_array[4][2], "D")

    def test_mental_array_module_correctly_insert_multiple_proposition_for_same_cell(self):
        mental_array_module = self.create_mental_array_module()
        north_relation = North()

        mental_array_module.insert_proposition(north_relation, "A", "B")
        mental_array_module.insert_proposition(north_relation, "A", "C")

        self.assertEqual(len(mental_array_module.objects), 3)
        self.assertEqual(mental_array_module.spatial_array[2][4], "A")
        self.assertEqual(mental_array_module.spatial_array[4][4], "B")
        self.assertEqual(mental_array_module.spatial_array[5][4], "C")
    
    def create_mental_array_module(self):
        mental_array_module = MentalArrayModule()
        mental_array_module.SIZE = 9
        mental_array_module.MARKED_RELATION_DISTANCE_FROM_AGENT_TO_REFERENT = 1
        mental_array_module.MARKED_RELATION_DISTANCE_FROM_REFERENT_TO_AGENT = 1
        mental_array_module.UNMARKED_RELATION_DISTANCE_FROM_AGENT_TO_REFERENT = 2
        mental_array_module.UNMARKED_RELATION_DISTANCE_FROM_REFERENT_TO_AGENT = 2
        mental_array_module.HIGH_AGENT_MEAN = 6
        mental_array_module.LOW_AGENT_MEAN = 2
        mental_array_module.REFERENT_MEAN  = 4
        mental_array_module.STANDARD_VARIATION = 0.75
        mental_array_module.AMOUNT_OF_FIRING_EVENTS = 10
        return mental_array_module