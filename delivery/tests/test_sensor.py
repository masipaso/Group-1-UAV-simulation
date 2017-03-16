import unittest
from delivery.agents.uav.Uav import Uav
from delivery.agents.BaseStation import BaseStation
from delivery.model.Worldmodel import WorldModel
from delivery.agents.uav.components.Sensor import Sensor


class SensorTest(unittest.TestCase):

    def setUp(self):
        self.model = WorldModel()
        self.base_station = BaseStation(model=self.model, pos=(200, 200, 200), bid=1, center=(200, 200, 200),
                                        range_of_base_station=250)
        # Create the uav
        position = self.base_station.get_pos()

        self.uav = Uav(self.model, pos=position, uid=2, max_charge=1000, battery_low=500,
                       base_station=self.base_station, battery_decrease_per_step=1,
                       battery_increase_per_step=10, max_altitude=4, sensor_range=5)

        self.sensor = Sensor(self.model.schedule.agents_by_type[Uav], self.model.landscape, self.uav.perceived_world, 5)

        self.uav.sensor = self.sensor

    def test_init(self):
        self.assertIs(self.sensor.perceived_world, self.uav.perceived_world)
        self.assertIs(self.sensor.agents, self.model.schedule.agents_by_type[Uav])
        self.assertIs(self.sensor.landscape, self.model.landscape)
        self.assertIs(self.sensor.sensor_range, 5)

    def test_is_out_of_bounds(self):
        # 1st Test: Valid value. Expected: False
        self.assertFalse(self.sensor.is_out_of_bounds((1, 1, 1)))

        # 2nd Test: Too big value. Expected: True
        self.assertTrue(self.sensor.is_out_of_bounds((10000, 10000, 1)))

        # 3rd Test: Negative Value. Expected: True
        self.assertTrue(self.sensor.is_out_of_bounds((-10000, -10000, 1)))

    def test_is_obstacle_at(self):
        # Test if there is an obstacle
        self.assertEqual(self.sensor.landscape.is_obstacle_at((10, 10), 1), self.sensor.is_obstacle_at((10, 10, 1)))
