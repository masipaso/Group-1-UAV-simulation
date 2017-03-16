import unittest
from delivery.agents.uav.Uav import Uav
from delivery.agents.BaseStation import BaseStation
from delivery.model.Worldmodel import WorldModel
from delivery.agents.uav.components.CommunicationModule import CommunicationModule


class CommunicationModuleTest(unittest.TestCase):

    def setUp(self):
        self.model = WorldModel()
        self.base_station = BaseStation(model=self.model, pos=(200, 200, 200), bid=1, center=(200, 200, 200),
                                        range_of_base_station=250)
        pos_x, pos_y, pos_z = self.base_station.get_pos()
        # Create the UAV
        position = (pos_x, pos_y, pos_z)
        self.uav = Uav(self.model, pos=position, uid=1, max_charge=1000, battery_low=500,
                       base_station=self.base_station, battery_decrease_per_step=1,
                       battery_increase_per_step=10, max_altitude=4, sensor_range=5)

        self.uav2 = Uav(self.model, pos=position, uid=2, max_charge=1000, battery_low=500,
                        base_station=self.base_station, battery_decrease_per_step=1,
                        battery_increase_per_step=10, max_altitude=4, sensor_range=5)

        self.comm_module = CommunicationModule(perceived_world=self.uav2.perceived_world, max_altitude=3)

        self.uav2.communication_module = self.comm_module

    def test_init(self):

        self.assertIs(self.comm_module.perceived_world, self.uav2.perceived_world)
        self.assertIs(self.comm_module.max_altitude, 3)

    def test_send_perceived_world(self):
        self.assertEqual(self.uav2.perceived_world, self.comm_module.send_perceived_world())

    def test__receive_perceived_world_from(self):
        # Test if I receive the other UAV's perceived world
        self.assertIs(self.comm_module._receive_perceived_world_from(self.uav),self.uav.perceived_world)

    def test_exchange_grid(self):
        # 1st Test: Test after 0 steps if I receive the correct value (conjunction of both UAV's dicts)
        self.comm_module.exchange_grid_with(self.uav)
        for altitude in range(0, self.comm_module.max_altitude):
            self.assertEqual(self.comm_module.perceived_world.perceived_world[altitude],
                             {**self.comm_module.perceived_world.perceived_world[altitude],
                              **self.uav.perceived_world.perceived_world[altitude]})
