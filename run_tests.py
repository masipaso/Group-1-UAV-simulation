from delivery.tests.test_baseStation import baseStationTest
import unittest

baseStation_result = unittest.TestResult()
baseStation_suite = unittest.TestSuite()
baseStation_suite.addTest(baseStationTest('test_create_item'))
baseStation_suite.addTest(baseStationTest('test_get_item'))
baseStation_suite.addTest(baseStationTest('test_get_number_of_items'))



baseStation_suite.run(result=baseStation_result)
print('Testing BaseStation. Result: {}'.format(baseStation_result))



