from delivery.tests.test_base_station import BaseStationTest
from delivery.tests.test_uav import UAVTest
from delivery.tests.test_world_model import WorldModelTest
from delivery.tests.test_static_grid import StaticGridTest
from delivery.tests.test_item import ItemTest
from delivery.tests.test_battery import BatteryTest
from delivery.tests.test_cargo_bay import CargoBayTest
from delivery.tests.test_communication_module import CommunicationModuleTest
from delivery.tests.test_sensor import SensorTest
from delivery.tests.test_flight_controller import FlightControllerTest

import sys

import unittest


class OutputHider:
    def __init__(self):
        self.save_stdout = None

    def hide_output(self):
        self.save_stdout = sys.stdout
        sys.stdout = open('trash', 'w')

    def un_hide_output(self):
        sys.stdout = self.save_stdout


class TestRunner:
    @staticmethod
    def create_cargo_bay_test_suite():
        suite = unittest.TestSuite()
        suite.addTest(CargoBayTest('test_init'))
        suite.addTest(CargoBayTest('test_is_empty'))
        suite.addTest(CargoBayTest('test_store_item'))
        suite.addTest(CargoBayTest('test_remove_item'))
        suite.addTest(CargoBayTest('test_get_destination'))
        suite.addTest(CargoBayTest('test_get_item'))
        return suite

    @staticmethod
    def create_base_station_test_suite():
        suite = unittest.TestSuite()
        suite.addTest(BaseStationTest('test_init'))
        suite.addTest(BaseStationTest('test_step'))
        suite.addTest(BaseStationTest('test_create_item'))
        suite.addTest(BaseStationTest('test_get_item'))
        suite.addTest(BaseStationTest('test_get_number_of_items'))
        suite.addTest(BaseStationTest('test_sort_items_by_priority'))
        suite.addTest(BaseStationTest('test_get_pos'))
        return suite

    @staticmethod
    def create_uav_test_suite():
        suite = unittest.TestSuite()
        suite.addTest(UAVTest('test_init'))
        suite.addTest(UAVTest('test_pickup_item'))
        suite.addTest(UAVTest('test_deliver_item'))
        suite.addTest(UAVTest('test_check_battery'))
        suite.addTest(UAVTest('test_arrive_at_base_station'))
        return suite

    @staticmethod
    def create_world_model_test_suite():
        suite = unittest.TestSuite()
        suite.addTest(WorldModelTest('test_init'))
        suite.addTest(WorldModelTest('test_compute_item_average_lifetime'))
        suite.addTest(WorldModelTest('test_compute_number_of_items'))
        suite.addTest(WorldModelTest('test_compute_number_of_picked_up_items'))
        suite.addTest(WorldModelTest('test_compute_number_of_delivered_items'))
        suite.addTest(WorldModelTest('test_compute_average_walk_length'))
        suite.addTest(WorldModelTest('test_compute_standard_deviation_walk_lengths'))
        suite.addTest(WorldModelTest('test_compute_walk_length_divided_by_distance'))
        return suite

    @staticmethod
    def create_static_grid_test_suite():
        suite = unittest.TestSuite()
        suite.addTest(StaticGridTest('test_init'))
        suite.addTest(StaticGridTest('test_get_neighborhood'))
        suite.addTest(StaticGridTest('test_out_of_bounds'))
        suite.addTest(StaticGridTest('test_place_obstacle'))
        suite.addTest(StaticGridTest('test_place_base_station'))
        suite.addTest(StaticGridTest('test_is_cell_empty'))
        suite.addTest(StaticGridTest('test_place_agent'))
        suite.addTest(StaticGridTest('test_is_obstacle_at'))
        suite.addTest(StaticGridTest('test_is_base_station_at'))
        return suite

    @staticmethod
    def create_item_test_suite():
        suite = unittest.TestSuite()
        suite.addTest(ItemTest('test_init'))
        suite.addTest(ItemTest('test_get_lifetime'))
        suite.addTest(ItemTest('test_step'))
        suite.addTest(ItemTest('test_set_delivered'))
        suite.addTest(ItemTest('test_get_destination'))
        return suite

    @staticmethod
    def create_battery_test_suite():
        suite = unittest.TestSuite()
        suite.addTest(BatteryTest('test_init'))
        suite.addTest(BatteryTest('test_charge'))
        suite.addTest(BatteryTest('test_discharge'))
        suite.addTest(BatteryTest('test_is_low'))
        suite.addTest(BatteryTest('test_is_empty'))
        suite.addTest(BatteryTest('test_is_charged'))
        suite.addTest(BatteryTest('test_get_charge'))
        return suite

    @staticmethod
    def create_communication_module_test_suite():
        suite = unittest.TestSuite()
        suite.addTest(CommunicationModuleTest('test_init'))
        suite.addTest(CommunicationModuleTest('test_send_perceived_world'))
        suite.addTest(CommunicationModuleTest('test__receive_perceived_world_from'))
        suite.addTest(CommunicationModuleTest('test_exchange_grid'))
        return suite

    @staticmethod
    def create_sensor_test_suite():
        suite = unittest.TestSuite()
        suite.addTest(SensorTest('test_init'))
        suite.addTest(SensorTest('test_is_out_of_bounds'))
        suite.addTest(SensorTest('test_is_obstacle_at'))
        return suite

    @staticmethod
    def create_flight_controller_test_suite():
        suite = unittest.TestSuite()
        suite.addTest(FlightControllerTest('test_init'))
        suite.addTest(FlightControllerTest('test_move_to'))
        return suite

    # Run Tests
    def run_tests(self):
        # Creating Results
        hider = OutputHider()
        result = unittest.TestResult()
        print("Running Tests")

        print("Testing Battery")
        hider.hide_output()
        self.create_battery_test_suite().run(result=result)
        hider.un_hide_output()

        print("Testing CargoBay")
        hider.hide_output()
        self.create_cargo_bay_test_suite().run(result=result)
        hider.un_hide_output()

        print("Testing BaseStation")
        hider.hide_output()
        self.create_base_station_test_suite().run(result=result)
        hider.un_hide_output()

        print("Testing UAV")
        hider.hide_output()
        self.create_uav_test_suite().run(result=result)
        hider.un_hide_output()

        print("Testing WorldModel")
        hider.hide_output()
        self.create_world_model_test_suite().run(result=result)
        hider.un_hide_output()

        print("Testing StaticGrid")
        hider.hide_output()
        self.create_static_grid_test_suite().run(result=result)
        hider.un_hide_output()

        print("Testing Item")
        hider.hide_output()
        self.create_item_test_suite().run(result=result)
        hider.un_hide_output()

        print("Testing CommunicationModule")
        hider.hide_output()
        self.create_communication_module_test_suite().run(result=result)
        hider.un_hide_output()

        print("Testing Sensor")
        hider.hide_output()
        self.create_sensor_test_suite().run(result=result)
        hider.un_hide_output()

        print("Testing FlightController")
        hider.hide_output()
        self.create_flight_controller_test_suite().run(result=result)
        hider.un_hide_output()

        print('\033[1mTest results (Summary): {}\033[0m'.format(result))

        print("\033[1mList of errors (if any):\033[0m")
        if result.errors:
            for err in result.errors:
                print("\033[1m\033[31mError\033[0m: {}".format(err))

        print("\033[1mList of failures (if any):\033[0m")
        if result.failures:
            for fail in result.failures:
                print("\033[1m\033[31mFailure\033[0m: {}".format(fail))
