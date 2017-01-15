import unittest
from delivery.algorithms.repellentAlgorithm import Algorithm
from delivery.agents.baseStation import BaseStation
from delivery.model.worldmodel import WorldModel
from delivery.agents.uav.uav import Uav


class repellentAlgorithm_Test(unittest.TestCase):

    def setUp(self):
        self.model = WorldModel()
        self.baseStation = BaseStation(model=self.model, pos=(200, 200), id=1, center=(200, 200),
                                       range_of_base_station=250)
        self.uav = Uav(model=self.model, pos=(200, 200), uid=1, max_battery=1000, battery_low=20,
                       base_station=self.baseStation)
        self.algorithm = Algorithm(uav=self.uav)
        self.uav.algorithm = self.algorithm

    def test_init(self):
        self.assertEqual(self.algorithm.uav, self.uav)
