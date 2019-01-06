import unittest
from unittest import mock
from mock import call, patch
from MentalArrayModule import MentalArrayModule
from Relation import *

class TestMentalArrayModule(unittest.TestCase):
    
    def test_mental_array_module_initialize_correctly(self):
        mental_array_module = self.create_mental_array_module()
        self.assertEqual(len(mental_array_module.objects), 0)

    @patch('MentalArrayModule.MentalArrayModule.add_new_object_to_spatial_array')
    @patch('MentalArrayModule.MentalArrayModule.add_object_by_reference_object_and_lxr_units')  
    def test_mental_array_module_should_call_correct_methods_for_new_proposition(self, mock_add_object_by_reference_object_and_lxr_units, mock_add_new_object_to_spatial_array):
        mental_array_module = self.create_mental_array_module()
        north_relation = North()
        west_relation = West()

        mental_array_module.insert_proposition(north_relation, "A", "B")
        mental_array_module.insert_proposition(north_relation, "B", "C")
        mental_array_module.insert_proposition(west_relation, "D", "C")
        mock_add_new_object_to_spatial_array.assert_has_calls([call(north_relation, "A", True), call(north_relation, "B", False)]) 
        mock_add_object_by_reference_object_and_lxr_units.assert_has_calls([call(north_relation, "B","C", False)])
        mock_add_object_by_reference_object_and_lxr_units.assert_has_calls([call(west_relation, "C", "D", True)])     


    @patch('MentalArrayModule.MentalArrayModule.add_new_object_to_spatial_array')
    def test_mental_array_module_should_call_correct_methods_for_multiple_propositions(self, mock_add_new_object_to_spatial_array):
        mental_array_module = self.create_mental_array_module()
        north_relation = North()

        mental_array_module.insert_proposition(north_relation, "A", "B")
        mock_add_new_object_to_spatial_array.assert_has_calls([call(north_relation, "A", True), call(north_relation, "B", False)])   

    def test_calculate_new_index_with_size_9(self):
        mental_array_module = self.create_mental_array_module()

        self.assertEqual(mental_array_module.calculate_new_index(1, 7), 8)
        self.assertEqual(mental_array_module.calculate_new_index(1, 9), -1)
        self.assertEqual(mental_array_module.calculate_new_index(3, -1), 2)
        self.assertEqual(mental_array_module.calculate_new_index(1, -7), -1)
        self.assertEqual(mental_array_module.calculate_new_index(2, -2), 0)

    def test_calculate_new_index_with_larger_grid_size(self):
        mental_array_module = self.create_mental_array_module_with_larger_grid()

        self.assertEqual(mental_array_module.calculate_new_index(1, 12), 13)
        self.assertEqual(mental_array_module.calculate_new_index(0, 9), 9)
        self.assertEqual(mental_array_module.calculate_new_index(3, -8), -1)
        self.assertEqual(mental_array_module.calculate_new_index(9, -7), 2)

    def test_map_direction_to_lxr_units(self):
        mental_array_module = self.create_mental_array_module()
        self.assertEqual(mental_array_module.map_direction_to_lxr_units(Direction.Plus, True), mental_array_module.marked_distance)
        self.assertEqual(mental_array_module.map_direction_to_lxr_units(Direction.Minus, True), -1 * mental_array_module.marked_distance)
        self.assertEqual(mental_array_module.map_direction_to_lxr_units(Direction.Zero, True), 0)
        self.assertEqual(mental_array_module.map_direction_to_lxr_units(Direction.Plus, False), mental_array_module.unmarked_distance)
        self.assertEqual(mental_array_module.map_direction_to_lxr_units(Direction.Minus, False), -1* mental_array_module.unmarked_distance)
        self.assertEqual(mental_array_module.map_direction_to_lxr_units(Direction.Zero, False), 0)
    
    def test_calculate_location_for_new_object(self):
        mental_array_module = self.create_mental_array_module()
        self.assertEqual(mental_array_module.calculate_location_for_new_object(West(), True), 2)
        self.assertEqual(mental_array_module.calculate_location_for_new_object(West(), False), 4)
        self.assertEqual(mental_array_module.calculate_location_for_new_object(SouthEast(), True), 6)
        self.assertEqual(mental_array_module.calculate_location_for_new_object(SouthEast(), False), 4)

    @patch('MentalArrayModule.MentalArrayModule.calculate_location_with_gaussian_distribution')
    def test_calculate_location_for_new_object_calls_the_correct_method(self, mock_calculate_location_with_gaussian_distribution):
        mental_array_module = self.create_mental_array_module()
        mental_array_module.calculate_location_for_new_object(West(), True)
        mental_array_module.calculate_location_for_new_object(West(), False)
        mental_array_module.calculate_location_for_new_object(SouthEast(), True)
        mental_array_module.calculate_location_for_new_object(SouthEast(), False)
        mock_calculate_location_with_gaussian_distribution.has_calls([call(6), call(2), call(4), call(2)])

    @patch('MentalArrayModule.MentalArrayModule.add_object_to_next_empty_cell')
    @patch('MentalArrayModule.MentalArrayModule.map_direction_to_lxr_units')
    @patch('MentalArrayModule.MentalArrayModule.calculate_new_index')  
    def test_add_object_by_lxr_units_without_need_look_for_next_empty_cell_has_correct_calls(self, mock_calculate_new_index, mock_map_direction_to_lxr_units, mock_add_object_to_next_empty_cell):
        mental_array_module = self.create_mental_array_module()
        mental_array_module.spatial_array.itemset((4,4), "A")
        south_east_relation = SouthEast()

        mental_array_module.add_object_by_reference_object_and_lxr_units(south_east_relation, "A", "B", True)

        mock_map_direction_to_lxr_units.assert_has_calls([call(Direction.Plus, True), call(Direction.Plus, True)])
        mock_calculate_new_index.assert_has_calls([call(4, mock_map_direction_to_lxr_units()), call(4, mock_map_direction_to_lxr_units())])
        mock_add_object_to_next_empty_cell.assert_not_called()

    @patch('MentalArrayModule.MentalArrayModule.add_object_to_next_empty_cell')
    @patch('MentalArrayModule.MentalArrayModule.map_direction_to_lxr_units')
    @patch('MentalArrayModule.MentalArrayModule.calculate_new_index')  
    def test_add_object_by_lxr_units_with_need_look_for_next_empty_cell_has_correct_calls(self, mock_calculate_new_index, mock_map_direction_to_lxr_units, mock_add_object_to_next_empty_cell):
        mental_array_module = self.create_mental_array_module()
        mental_array_module.spatial_array.itemset((4,4), "A")
        mental_array_module.spatial_array.itemset((6,6), "B")
        south_east_relation = SouthEast()

        mental_array_module.add_object_by_reference_object_and_lxr_units(south_east_relation, "A", "C", True)

        mock_map_direction_to_lxr_units.assert_has_calls([call(Direction.Plus, True), call(Direction.Plus, True)])
        mock_calculate_new_index.assert_has_calls([call(4, mock_map_direction_to_lxr_units()), call(4, mock_map_direction_to_lxr_units())])
        mock_add_object_to_next_empty_cell.has_calls([call(6, 6, south_east_relation, "C", True)])

    def test_normalize_lxr_units(self):
        mental_array_module = self.create_mental_array_module()
        self.assertEqual(mental_array_module.normalize_lxr_units(-2), -1)
        self.assertEqual(mental_array_module.normalize_lxr_units(-5), -1)
        self.assertEqual(mental_array_module.normalize_lxr_units(1), 1)
        self.assertEqual(mental_array_module.normalize_lxr_units(2), 1)
        self.assertEqual(mental_array_module.normalize_lxr_units(0), 0)

    def test_add_object_by_lxr_units_without_need_look_for_next_empty_cell(self):
        mental_array_module = self.create_mental_array_module()
        mental_array_module.spatial_array.itemset((4,4), "A")
        south_east_relation = SouthEast()

        mental_array_module.add_object_by_reference_object_and_lxr_units(south_east_relation, "A", "B", True)
        self.assertEqual(mental_array_module.spatial_array[6][6], "B")


    def test_add_object_to_next_empty_cell(self):
        mental_array_module = self.create_mental_array_module()
        mental_array_module.spatial_array.itemset((4,4), "A")
        mental_array_module.spatial_array.itemset((5,5), "B")
        mental_array_module.spatial_array.itemset((6,6), "C")
        mental_array_module.add_object_to_next_empty_cell(4, 4, 2, 2, "D")
        
        self.assertEqual(mental_array_module.spatial_array[7][7], "D")

    def test_add_object_to_next_empty_cell_and_no_empty_cell_found(self):
        mental_array_module = self.create_mental_array_module()
        mental_array_module.spatial_array.itemset((4,4), "A")
        mental_array_module.spatial_array.itemset((5,5), "B")
        mental_array_module.spatial_array.itemset((6,6), "C")
        mental_array_module.spatial_array.itemset((7,7), "D")
        mental_array_module.spatial_array.itemset((8,8), "E")
        mental_array_module.add_object_to_next_empty_cell(4, 4, 2, 2, "F")
        
        self.assertFalse(mental_array_module.objects.__contains__("F"))

    def test_mental_array_module_correctly_insert_new_proposition(self):
        mental_array_module = self.create_mental_array_module()
        north_relation = North()

        mental_array_module.insert_proposition(north_relation, "A", "B")
        self.assertEqual(len(mental_array_module.objects), 2)
        self.assertEqual(mental_array_module.spatial_array[2][4], "A")
        self.assertEqual(mental_array_module.spatial_array[4][4], "B")

    def test_mental_array_module_correctly_insert_new_proposition_for_intercardinal_direction(self):
        mental_array_module = self.create_mental_array_module()
        north_west_relation = NorthWest()

        mental_array_module.insert_proposition(north_west_relation, "A", "B")

        self.assertEqual(len(mental_array_module.objects), 2)
        self.assertEqual(mental_array_module.spatial_array[2][2], "A")
        self.assertEqual(mental_array_module.spatial_array[4][4], "B")

        mental_array_module = self.create_mental_array_module()
        north_east_relation = NorthEast()

        mental_array_module.insert_proposition(north_east_relation, "A", "B")

        self.assertEqual(len(mental_array_module.objects), 2)
        self.assertEqual(mental_array_module.spatial_array[2][6], "A")
        self.assertEqual(mental_array_module.spatial_array[4][4], "B")

        mental_array_module = self.create_mental_array_module()
        south_east_relation = SouthEast()

        mental_array_module.insert_proposition(south_east_relation, "A", "B")

        self.assertEqual(len(mental_array_module.objects), 2)
        self.assertEqual(mental_array_module.spatial_array[6][6], "A")
        self.assertEqual(mental_array_module.spatial_array[4][4], "B")

        mental_array_module = self.create_mental_array_module()
        south_west_relation = SouthWest()

        mental_array_module.insert_proposition(south_west_relation, "A", "B")

        self.assertEqual(len(mental_array_module.objects), 2)
        self.assertEqual(mental_array_module.spatial_array[6][2], "A")
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


    def test_mental_array_module_correctly_insert_multiple_proposition_with_intercardinal_directions(self):
        mental_array_module = self.create_mental_array_module()
        north_west_relation = NorthWest()
        south_west_relation = SouthWest()
        south_east_relation = SouthEast()
        north_east_relation = NorthEast()

        mental_array_module.insert_proposition(north_west_relation, "A", "B")
        mental_array_module.insert_proposition(south_west_relation, "C", "B")
        mental_array_module.insert_proposition(south_east_relation, "D", "B")
        mental_array_module.insert_proposition(north_east_relation, "E", "C")
        self.assertEqual(len(mental_array_module.objects), 5)
        self.assertEqual(mental_array_module.spatial_array[2][2], "A")
        self.assertEqual(mental_array_module.spatial_array[4][4], "B")
        self.assertEqual(mental_array_module.spatial_array[6][2], "C")
        self.assertEqual(mental_array_module.spatial_array[6][6], "D")
        self.assertEqual(mental_array_module.spatial_array[3][5], "E")
    

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


    def test_mental_array_module_correctly_insert_multiple_proposition_with_different_settings_for_marked_and_unmarked_relations(self):
        mental_array_module = self.create_mental_array_module_with_different_settings_for_marked_and_unmarked_relations()
        north_west_relation = NorthWest()
        south_west_relation = SouthWest()
        east_relation = East()
        west_relation = West()

        mental_array_module.insert_proposition(north_west_relation, "A", "B")
        mental_array_module.insert_proposition(south_west_relation, "C", "B")
        mental_array_module.insert_proposition(east_relation, "D", "B")
        mental_array_module.insert_proposition(west_relation, "E", "C")
        mental_array_module.insert_proposition(east_relation, "F", "B")
        mental_array_module.insert_proposition(east_relation, "G", "B")
        mental_array_module.insert_proposition(east_relation, "H", "B")

        self.assertEqual(len(mental_array_module.objects), 7)
        self.assertEqual(mental_array_module.spatial_array[3][3], "A")
        self.assertEqual(mental_array_module.spatial_array[4][4], "B")
        self.assertEqual(mental_array_module.spatial_array[5][3], "C")
        self.assertEqual(mental_array_module.spatial_array[4][6], "D")
        self.assertEqual(mental_array_module.spatial_array[5][1], "E")
        self.assertEqual(mental_array_module.spatial_array[4][7], "F")
        self.assertEqual(mental_array_module.spatial_array[4][8], "G")


    def test_mental_array_module_correctly_insert_multiple_proposition_with_different_settings_for_larger_grid(self):
        mental_array_module = self.create_mental_array_module_with_larger_grid()
        north_west_relation = NorthWest()
        south_west_relation = SouthWest()
        east_relation = East()
        west_relation = West()
        south_east_relation = SouthEast()

        mental_array_module.insert_proposition(north_west_relation, "A", "B")
        mental_array_module.insert_proposition(south_west_relation, "C", "B")
        mental_array_module.insert_proposition(east_relation, "D", "B")
        mental_array_module.insert_proposition(west_relation, "E", "C")
        mental_array_module.insert_proposition(south_east_relation, "F", "C")
        mental_array_module.insert_proposition(south_east_relation, "G", "C")
        mental_array_module.insert_proposition(south_east_relation, "H", "C")
        mental_array_module.insert_proposition(south_east_relation, "I", "C")
        mental_array_module.insert_proposition(south_east_relation, "J", "C")
        mental_array_module.insert_proposition(south_east_relation, "K", "H")

        self.assertEqual(len(mental_array_module.objects), 10)
        self.assertEqual(mental_array_module.spatial_array[7][7], "A")
        self.assertEqual(mental_array_module.spatial_array[10][10], "B")
        self.assertEqual(mental_array_module.spatial_array[13][7], "C")
        self.assertEqual(mental_array_module.spatial_array[10][13], "D")
        self.assertEqual(mental_array_module.spatial_array[13][4], "E")
        self.assertEqual(mental_array_module.spatial_array[16][10], "F")
        self.assertEqual(mental_array_module.spatial_array[17][11], "G")
        self.assertEqual(mental_array_module.spatial_array[18][12], "H")
        self.assertEqual(mental_array_module.spatial_array[19][13], "I")
        self.assertEqual(mental_array_module.spatial_array[20][14], "J")

    def create_mental_array_module(self):
        mental_array_module = MentalArrayModule()
        mental_array_module.start(9, 2, 2, 0.0, 10)

        return mental_array_module

    def create_mental_array_module_with_different_settings_for_marked_and_unmarked_relations(self):
        mental_array_module = MentalArrayModule()
        mental_array_module.start(9, 2, 1, 0.0, 10)

        return mental_array_module

    def create_mental_array_module_with_larger_grid(self):
        mental_array_module = MentalArrayModule()
        mental_array_module.start(21, 3, 3, 0.0, 10)

        return mental_array_module