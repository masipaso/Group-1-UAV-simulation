from delivery.tests.test_baseStation import baseStation_Test
from delivery.tests.test_uav import UAV_test
from delivery.tests.test_worldmodel import worldModel_Test
from delivery.tests.test_repellent import repellent_Test
from delivery.tests.test_static_grid import staticGrid_Test
from delivery.tests.test_item import Item_Test
from delivery.tests.test_repellentAlgorithm import repellentAlgorithm_Test
import sys

import unittest

class output_hider():
    def __init__(self):
        self.save_stdout = None

    def hide_output(self):
        self.save_stdout = sys.stdout
        sys.stdout = open('trash', 'w')

    def unhide_output(self):
        sys.stdout = self.save_stdout

class tests_runner():
    def create_BaseStation_suite(self):
         # Creating Test Suite
        suite = unittest.TestSuite()
        suite.addTest(baseStation_Test('test_init'))
        suite.addTest(baseStation_Test('test_create_item'))
        suite.addTest(baseStation_Test('test_get_item'))
        suite.addTest(baseStation_Test('test_get_number_of_items'))
        suite.addTest(baseStation_Test('test_sort_items_by_priority'))
        suite.addTest(baseStation_Test('test_get_pos'))
        return suite

    def create_UAV_suite(self):
        # Creating Test Suite
        suite = unittest.TestSuite()
        suite.addTest(UAV_test('test_init'))
        suite.addTest(UAV_test('test_pickup_item'))
        suite.addTest(UAV_test('test_deliver_item'))
        suite.addTest(UAV_test('test_check_battery'))
        suite.addTest(UAV_test('test_charge_battery'))
        suite.addTest(UAV_test('test_arrive_at_base_station'))
        suite.addTest(UAV_test('test_move_to'))
        suite.addTest(UAV_test('test_get_euclidean_distance'))
        suite.addTest(UAV_test('test_get_grid'))
        suite.addTest(UAV_test('test_find_uavs_close'))
        suite.addTest(UAV_test('test_get_nearest_base_station'))
        return suite

    def create_WorldModel_test_suite(self):
        # Creating Test Suite
        suite = unittest.TestSuite()
        suite.addTest(worldModel_Test('test_init'))
        suite.addTest(worldModel_Test('test_compute_item_average_lifetime'))
        suite.addTest(worldModel_Test('test_compute_number_of_items'))
        suite.addTest(worldModel_Test('test_compute_number_of_picked_up_items'))
        suite.addTest(worldModel_Test('test_compute_number_of_delivered_items'))
        suite.addTest(worldModel_Test('test_compute_average_walk_length'))
        suite.addTest(worldModel_Test('test_compute_standard_deviation_walk_lengths'))
        suite.addTest(worldModel_Test('test_compute_walk_length_divided_by_distance'))
        suite.addTest(worldModel_Test('test_create_base_station'))
        suite.addTest(worldModel_Test('test_create_uav'))
        return suite

    def create_Repellent_suite(self):
        # Creating Test Suite
        suite = unittest.TestSuite()
        suite.addTest(repellent_Test('test_init'))
        suite.addTest(repellent_Test('test_step'))
        suite.addTest(repellent_Test('test_weaken'))
        suite.addTest(repellent_Test('test_strengthen'))
        suite.addTest(repellent_Test('test_get_position'))
        return suite

    def create_StaticGrid_suite(self):
        # Creating Test Suite
        suite = unittest.TestSuite()
        suite.addTest(staticGrid_Test('test_init'))
        suite.addTest(staticGrid_Test('test_get_neighborhood'))
        suite.addTest(staticGrid_Test('test_out_of_bounds'))
        suite.addTest(staticGrid_Test('test_place_obstacle'))
        suite.addTest(staticGrid_Test('test_place_base_station'))
        suite.addTest(staticGrid_Test('test_is_cell_empty'))
        suite.addTest(staticGrid_Test('test_place_agent'))
        suite.addTest(staticGrid_Test('test_is_obstacle_at'))
        suite.addTest(staticGrid_Test('test_is_base_station_at'))
        return suite

    def create_Item_test_suite(self):
        # Creating Test Suite
        suite = unittest.TestSuite() # test_get_lifetime
        suite.addTest(Item_Test('test_init'))
        suite.addTest(Item_Test('test_get_lifetime'))
        suite.addTest(Item_Test('test_step'))
        suite.addTest(Item_Test('test_deliver'))
        suite.addTest(Item_Test('test_get_destination'))
        return suite

    def create_RepellenAlgorithm_test_suite(self):
        # Creating Test Suite
        suite = unittest.TestSuite()
        suite.addTest(repellentAlgorithm_Test('test_init'))
        #suite.addTest(Obstacle_Test('test_get_position'))
        return suite

    # Run Tests
    def run_tests(self):
        # Creating Results
        hider = output_hider()
        result = unittest.TestResult()
        print("Running Tests")
        print("Testing BaseStation")
        hider.hide_output()

        self.create_BaseStation_suite().run(result=result)
        hider.unhide_output()

        print("Testing UAV")
        hider.hide_output()

        self.create_UAV_suite().run(result=result)
        hider.unhide_output()

        print("Testing TwoMultiGrid")
        hider.hide_output()

        self.create_TwoMultiGrid_test_suite().run(result=result)
        hider.unhide_output()

        print("Testing WorldModel")
        hider.hide_output()

        self.create_WorldModel_test_suite().run(result=result)
        hider.unhide_output()

        print("Testing Repellent")
        hider.hide_output()

        self.create_Repellent_suite().run(result=result)
        hider.unhide_output()

        print("Testing StaticGrid")
        hider.hide_output()

        self.create_StaticGrid_suite().run(result=result)
        hider.unhide_output()

        print("Testing Item")
        hider.hide_output()

        self.create_Item_test_suite().run(result=result)
        hider.unhide_output()

        print("Testing Obstacle")
        hider.hide_output()

        self.create_Obstacle_test_suite().run(result=result)
        hider.unhide_output()

        print("Testing RepellentAlgorithm")
        hider.hide_output()

        self.create_RepellenAlgorithm_test_suite().run(result=result)
        hider.unhide_output()

        print('\033[1mTest results (Summary): {}\033[0m'.format(result))

        print("\033[1mList of errors (if any):\033[0m")
        if result.errors != []:
            for err in result.errors:
                print("\033[1m\033[31mError\033[0m: {}".format(err))

        print("\033[1mList of failures (if any):\033[0m")
        if result.failures != []:
            for fail in result.failures:
                print("\033[1m\033[31mFailure\033[0m: {}".format(fail))
