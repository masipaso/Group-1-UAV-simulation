from delivery.tests.test_baseStation import baseStation_Test
from delivery.tests.test_uav import UAV_test
from delivery.tests.test_multi_grids import TwoMultiGrid_test
from delivery.tests.test_worldmodel import worldModel_Test
from delivery.tests.test_repellent import repellent_Test
from delivery.tests.test_static_grid import staticGrid_Test
from delivery.tests.test_item import Item_Test
from delivery.tests.test_obstacle import Obstacle_Test

import unittest

# Creating Results
result = unittest.TestResult()

def create_BaseStation_suite():
    # Creating Test Suite
    suite = unittest.TestSuite()
    suite.addTest(baseStation_Test('test_init'))
    suite.addTest(baseStation_Test('test_create_item'))
    suite.addTest(baseStation_Test('test_get_item'))
    suite.addTest(baseStation_Test('test_get_number_of_items'))
    suite.addTest(baseStation_Test('test_sort_items_by_priority'))
    suite.addTest(baseStation_Test('test_get_pos'))
    return suite

def create_UAV_suite():
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
    return suite

def create_TwoMultiGrid_test_suite():
    # Creating Test Suite
    suite = unittest.TestSuite()
    suite.addTest(TwoMultiGrid_test('test_init'))
    suite.addTest(TwoMultiGrid_test('test_move_agent'))
    suite.addTest(TwoMultiGrid_test('test_get_repellent_on'))
    return suite

def create_WorldModel_test_suite():
    # Creating Test Suite
    suite = unittest.TestSuite()
    suite.addTest(worldModel_Test('test_init'))
    suite.addTest(worldModel_Test('test_create_base_station'))
    suite.addTest(worldModel_Test('test_create_uav'))
    return suite

def create_Repellent_suite():
    # Creating Test Suite
    suite = unittest.TestSuite()
    suite.addTest(repellent_Test('test_init'))
    suite.addTest(repellent_Test('test_step'))
    suite.addTest(repellent_Test('test_weaken'))
    suite.addTest(repellent_Test('test_strengthen'))
    suite.addTest(repellent_Test('test_get_position'))
    return suite

def create_StaticGrid_suite():
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

def create_Item_test_suite():
    # Creating Test Suite
    suite = unittest.TestSuite()
    suite.addTest(Item_Test('test_init'))
    suite.addTest(Item_Test('test_deliver'))
    suite.addTest(Item_Test('test_get_destination'))
    return suite

def create_Obstacle_test_suite():
    # Creating Test Suite
    suite = unittest.TestSuite()
    suite.addTest(Obstacle_Test('test_init'))
    suite.addTest(Obstacle_Test('test_get_position'))

    return suite

# Run Tests
print("Running Tests")
create_BaseStation_suite().run(result=result)
create_UAV_suite().run(result=result)
create_TwoMultiGrid_test_suite().run(result=result)
create_WorldModel_test_suite().run(result=result)
create_Repellent_suite().run(result=result)
create_StaticGrid_suite().run(result=result)
create_Item_test_suite().run(result=result)
create_Obstacle_test_suite().run(result=result)

print("\n"*5)


print('\033[1mTest results (Summary): {}\033[0m'.format(result))

print("\033[1mList of errors (if any):\033[0m")
if result.errors != []:
    for err in result.errors:
        print("\033[1m\033[31mError\033[0m: {}".format(err))

print("\n")
print("\033[1mList of failures (if any):\033[0m")
if result.failures != []:
    for fail in result.failures:
        print("\033[1m\033[31mFailure\033[0m: {}".format(fail))