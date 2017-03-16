from delivery.model.Worldmodel import WorldModel
from delivery.agents.BaseStation import BaseStation
from delivery.agents.uav.Uav import Uav
import configparser
import unittest
from mesa.datacollection import DataCollector
from delivery.schedule.Schedule import Schedule
import numpy as np


class WorldModelTest(unittest.TestCase):

    def setUp(self):
        self.model = WorldModel()

    def test_init(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.assertEqual(self.model.width, config.getint('Grid', 'width', fallback=500))
        self.assertEqual(self.model.height, config.getint('Grid', 'height', fallback=500))
        self.assertEqual(self.model.pixel_ratio, config.getint('Grid', 'pixel_ratio', fallback=10))
        self.assertEqual(self.model.background_image_source, config.get('Grid', 'image',
                                                                        fallback='./delivery/visualization/images/a_city500x500.jpg'))
        self.assertEqual(self.model.range_of_base_station, config.getfloat('Base_station', 'range_of_base_station',
                                                                           fallback=125))
        self.assertEqual(self.model.number_of_uavs_per_base_station, config.getint('UAV', 'number_of_uavs_per_base_station',
                                                                                   fallback=2))
        self.assertEqual(self.model.max_charge, config.getint('UAV', 'max_charge', fallback=1000))
        self.assertEqual(self.model.battery_low, config.getint('UAV', 'battery_low', fallback=500))

        self.assertEqual(self.model.landscape.width, config.getint('Grid', 'width', fallback=500))
        self.assertEqual(self.model.landscape.height, config.getint('Grid', 'height', fallback=500))
        self.assertEqual(self.model.number_of_delivered_items, 0)
        self.assertIsInstance(self.model.datacollector, DataCollector)
        self.assertIsInstance(self.model.schedule, Schedule)

        self.assertIsInstance(self.model.item_schedule, Schedule)

    def test_compute_number_of_items(self):
        # Hard to test with specific values. But at least can test if my self-computed values match the values from the method...
        # 1st Test: No items created. Value should be 0

        self.assertEqual(self.model.compute_number_of_items(self.model), 0)

        # Let us do some 50 steps
        for i in range(1, 50):
            self.model.step()

        # 2nd Test: Numbers should still match after 100 steps!
        number_of_items = 0
        for base_station in self.model.schedule.agents_by_type[BaseStation]:
            number_of_items += base_station.get_number_of_items()

        self.assertEqual(self.model.compute_number_of_items(self.model), number_of_items)

    def test_compute_number_of_picked_up_items(self):
        # Hard to test with specific values. But at least can test if my self-computed values match the values from the method..
        # 1st Test: No items created. Value should be 0
        self.assertEqual(self.model.compute_number_of_picked_up_items(self.model), 0)

        # Let us do some 50 steps
        for i in range(1, 50):
            self.model.step()

        # Make sure, we actually really created items at least..
        while self.model.compute_number_of_items(self.model) == 0:
            self.model.step()

        number_of_picked_up_items = 0
        for base_station in self.model.schedule.agents_by_type[BaseStation]:
            number_of_picked_up_items += base_station.get_number_of_items(picked_up=True)

        # 2nd Test: Numbers of picked up items
        self.assertEqual(self.model.compute_number_of_picked_up_items(self.model),number_of_picked_up_items)

    def test_compute_number_of_delivered_items(self):
        # Hard to test with specific values. But at least can test if my self-computed values match the values from the method..
        # 1st Test: no items created, none delivered. 0 should be result
        self.assertEqual(self.model.compute_number_of_delivered_items(self.model), 0)

        # Let us do some 50 steps
        for i in range(1, 50):
            self.model.step()

        # 2nd Test: Numbers should still match after 100 steps!
        self.assertEqual(self.model.compute_number_of_delivered_items(self.model),self.model.number_of_delivered_items)

    def test_compute_average_walk_length(self):
        # Hard to test with specific values. But at least can test if my self-computed values match the values from the method...
        # 1st Test: Result should be zero in the beginning
        self.assertEqual(self.model.compute_average_walk_length(self.model), 0)

        # 2nd Test: After 50 steps, result should be same as my own calculation
        for i in range(1, 50):
            self.model.step()

        average_walks = []
        for uav in self.model.schedule.agents_by_type[Uav]:
            for elem in uav.get_walk_lengths():
                average_walks.append(elem)
        if len(average_walks) > 0:
            walk_length = sum(average_walks) / len(average_walks)
        else:
            walk_length = 0

        self.assertEqual(self.model.compute_average_walk_length(self.model), walk_length)

    def test_compute_standard_deviation_walk_lengths(self):
        # Hard to test with specific values. But at least can test if my self-computed values match the values from the method...
        # 1st Test: Result should be zero in the beginning
        self.assertEqual(self.model.compute_standard_deviation_walk_lengths(self.model), 0)

        # 2nd Test: After 50 steps, result should be same as my own calculation
        for i in range(1, 50):
            self.model.step()

        average_walks = []
        for uav in self.model.schedule.agents_by_type[Uav]:
            for elem in uav.get_walk_lengths():
                average_walks.append(elem)
        if len(average_walks) > 0:
            stddev = np.std(average_walks)
        else:
            stddev = 0

        self.assertEqual(self.model.compute_standard_deviation_walk_lengths(self.model), stddev)

    def test_compute_walk_length_divided_by_distance(self):
        # Hard to test with specific values. But at least can test if my self-computed values match the values from the method...
        # 1st Test: Result should be zero in the beginning
        self.assertEqual(self.model.compute_walk_length_divided_by_distance(self.model), 0)

        # 2nd Test: After 50 steps, result should be same as my own calculation
        for i in range(1, 50):
            self.model.step()

        length_by_distance = []
        for uav in self.model.schedule.agents_by_type[Uav]:
            for elem in uav.get_walk_length_divided_by_initial_distance():
                length_by_distance.append(elem)
        if len(length_by_distance) > 0:
            result = sum(length_by_distance) / len(length_by_distance)
        else:
            result = 0

        self.assertEqual(self.model.compute_walk_length_divided_by_distance(self.model), result)

    def test_compute_item_average_lifetime(self):
        # Hard to test with specific values. But at least can test if my self-computed values match the values from the method...
        # 1st Test: Should be zero in the beginning
        self.assertEqual(self.model.compute_item_average_lifetime(self.model), 0)

        # After 50 steps, value should be changed
        for i in range(1, 50):
            self.model.step()

        result = 0
        for item in self.model.item_schedule.agents:
            result = result + item.lifetime

        # 2nd Test: After 50 steps...
        self.assertEqual(self.model.compute_item_average_lifetime(self.model), result/len(self.model.item_schedule.agents))
