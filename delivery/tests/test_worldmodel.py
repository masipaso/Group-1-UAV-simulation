from delivery.model.worldmodel import WorldModel
from delivery.agents.baseStation import BaseStation
from delivery.agents.uav import Uav

import unittest

class worldModel_Test(unittest.TestCase):
    def setUp(self):
        self.model = WorldModel()


    def test_create_base_station(self):
        # Test: Place a base station at any valid position
        # After that the base station must be in the scheduler and be placed on the landscape grid
        self.model.landscape.place_obstacle((30,30))
        self.model.create_base_station(123,(30,30))

        found = False
        base = None
        for elem in self.model.grid.get_cell_list_contents((30,30)):
            if isinstance(elem,BaseStation):
                found = True
                base = elem
                break

        self.assertTrue(found)

        self.assertTrue(self.model.landscape.is_base_station_at((30,30)))

        self.assertIn(base,self.model.schedule.agents)

    def test_create_uav(self):
        # Test: Place a uav at a valid position
        self.model.landscape.place_obstacle((30,30))
        self.model.create_base_station(123,(30,30))

        # Find the base station that we just placed
        base = None
        for elem in self.model.grid.get_cell_list_contents((30, 30)):
            if isinstance(elem, BaseStation):
                base = elem
                break

        self.model.create_uav(uid=123,base_station=base)

        # Find UAV in grid
        found = False
        uav = None
        for elem in self.model.grid.get_cell_list_contents((30, 30)):
            if isinstance(elem, Uav):
                uav = elem
                found = True
                break

        # Test: UAV is in grid
        self.assertTrue(found)

        # Test: UAV is in perceived_world_grid
        found = False
        uav = None
        for elem in self.model.perceived_world_grid.get_cell_list_contents((30, 30)):
            if isinstance(elem, Uav):
                uav = elem
                found = True
                break

        self.assertTrue(found)

        # Test: The UAV has to be added to the schedule
        self.assertIn(uav,self.model.schedule.agents)


