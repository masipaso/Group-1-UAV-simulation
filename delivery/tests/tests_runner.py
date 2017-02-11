from delivery.tests.test_baseStation import baseStation_Test
from delivery.tests.test_uav import UAV_test
from delivery.tests.test_worldmodel import worldModel_Test
from delivery.tests.test_static_grid import staticGrid_Test
from delivery.tests.test_item import Item_Test
from delivery.tests.test_battery import battery_Test
from delivery.tests.test_cargobay import cargoBay_Test

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
    def create_cargoBay_suite(self):
        suite = unittest.TestSuite()
        suite.addTest(cargoBay_Test('test_init'))
        suite.addTest(cargoBay_Test('test_is_empty'))
        suite.addTest(cargoBay_Test('test_store_item'))
        suite.addTest(cargoBay_Test('test_remove_item'))
        suite.addTest(cargoBay_Test('test_get_destination'))
        suite.addTest(cargoBay_Test('test_get_item'))
        return suite

    def create_BaseStation_suite(self):
         # Creating Test Suite
        suite = unittest.TestSuite()
        suite.addTest(baseStation_Test('test_init'))
        suite.addTest(baseStation_Test('test_step'))
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
        suite.addTest(UAV_test('test_arrive_at_base_station'))
        suite.addTest(UAV_test('test_find_uavs_close'))
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
        suite.addTest(Item_Test('test_set_delivered'))
        suite.addTest(Item_Test('test_get_destination'))
        return suite

    def create_Battery_suite(self):
         # Creating Test Suite
        suite = unittest.TestSuite()
        suite.addTest(battery_Test('test_init'))
        suite.addTest(battery_Test('test_charge'))
        suite.addTest(battery_Test('test_discharge'))
        suite.addTest(battery_Test('test_is_low'))
        suite.addTest(battery_Test('test_is_empty'))
        suite.addTest(battery_Test('test_is_charged'))
        suite.addTest(battery_Test('test_get_charge'))
        return suite

    # Run Tests
    def run_tests(self):
        # Creating Results
        hider = output_hider()
        result = unittest.TestResult()
        print("Running Tests")

        print("Testing Battery")
        hider.hide_output()
        self.create_Battery_suite().run(result=result)
        hider.unhide_output()

        print("Testing CargoBay")
        hider.hide_output()
        self.create_cargoBay_suite().run(result=result)
        hider.unhide_output()

        print("Testing BaseStation")
        hider.hide_output()
        self.create_BaseStation_suite().run(result=result)
        hider.unhide_output()
        #
        print("Testing UAV")
        hider.hide_output()
        self.create_UAV_suite().run(result=result)
        hider.unhide_output()

        print("Testing WorldModel")
        hider.hide_output()
        self.create_WorldModel_test_suite().run(result=result)
        hider.unhide_output()
        #
        print("Testing Repellent")
        hider.hide_output()
        self.create_Repellent_suite().run(result=result)
        hider.unhide_output()
        #
        print("Testing StaticGrid")
        hider.hide_output()
        self.create_StaticGrid_suite().run(result=result)
        hider.unhide_output()
        #
        print("Testing Item")
        hider.hide_output()
        self.create_Item_test_suite().run(result=result)
        hider.unhide_output()

        #print("Testing Obstacle")
        #hider.hide_output()
        #self.create_Obstacle_test_suite().run(result=result)
        #hider.unhide_output()
        #
        #print("Testing RepellentAlgorithm")
        #hider.hide_output()
        #self.create_RepellenAlgorithm_test_suite().run(result=result)
        #hider.unhide_output()


        print('\033[1mTest results (Summary): {}\033[0m'.format(result))

        print("\033[1mList of errors (if any):\033[0m")
        if result.errors != []:
            for err in result.errors:
                print("\033[1m\033[31mError\033[0m: {}".format(err))

        print("\033[1mList of failures (if any):\033[0m")
        if result.failures != []:
            for fail in result.failures:
                print("\033[1m\033[31mFailure\033[0m: {}".format(fail))
