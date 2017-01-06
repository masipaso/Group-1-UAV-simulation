from delivery.tests.test_baseStation import baseStation_Test
from delivery.tests.test_uav import UAV_test
from delivery.tests.test_multi_grids import TwoMultiGrid_test
from delivery.tests.test_worldmodel import worldModel_Test

import unittest

# Creating Results
result = unittest.TestResult()



def create_BaseStation_suite():
    # Creating Test Suite
    suite = unittest.TestSuite()
    suite.addTest(baseStation_Test('test_create_item'))
    suite.addTest(baseStation_Test('test_get_item'))
    suite.addTest(baseStation_Test('test_get_number_of_items'))
    return suite

def create_UAV_suite():
    # Creating Test Suite
    suite = unittest.TestSuite()
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
    suite.addTest(TwoMultiGrid_test('test_move_agent'))
    suite.addTest(TwoMultiGrid_test('test_get_repellent_on'))
    return suite

def create_WorldModel_test_suite():
    # Creating Test Suite
    suite = unittest.TestSuite()
    suite.addTest(worldModel_Test('test_create_base_station'))
    suite.addTest(worldModel_Test('test_create_uav'))
    return suite


# Run Tests
print("Running Tests")
#create_BaseStation_suite().run(result=result)
#create_UAV_suite().run(result=result)
#create_TwoMultiGrid_test_suite().run(result=result)
create_WorldModel_test_suite().run(result=result)


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