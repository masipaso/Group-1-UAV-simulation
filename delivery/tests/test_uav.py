import unittest
from delivery.agents.uav.Uav import Uav
from delivery.agents.Item import Item
from delivery.agents.BaseStation import BaseStation
from delivery.model.Worldmodel import WorldModel

class UAV_test(unittest.TestCase):

    def setUp(self):
        self.model = WorldModel()
        self.baseStation = BaseStation(model=self.model, pos=(200, 200), id=1, center=(200, 200), range_of_base_station=250)
        self.uav = Uav(model=self.model, pos=(200,200),uid=1,max_charge=1000,battery_low=20,battery_decrease_per_step=1,battery_increase_per_step=10,base_station=self.baseStation,altitude=5)

    def test_init(self):
        self.assertEqual(self.uav.model,self.model)
        self.assertEqual(self.uav.pos,(200,200))
        self.assertEqual(self.uav.uid,1)
        self.assertIsNone(self.uav.destination)
        self.assertEqual(self.uav.state,1)
        self.assertEqual(self.uav.base_station,self.baseStation)
        self.assertIsNotNone(self.uav.perceived_world_grid)

    def test_pickup_item(self):
        # 1st Test: item = None, result: state =1,  cargobay.item = None
        self.uav.state = 1
        self.uav.pick_up_item(item=None)
        self.assertEqual(self.uav.state,1)
        self.assertIsNone(self.uav.cargo_bay.item)

        # 2nd Test: item is Not None, result: state = 2, cargobay.item = item, item is in perceived_world_grid
        item = Item(destination=(0,0))
        self.uav.pick_up_item(item)
        self.assertEqual(self.uav.state,2)
        self.assertIs(self.uav.cargo_bay.item,item)
        self.assertIn(item,self.uav.perceived_world_grid.get_cell_list_contents(item.destination))
        self.assertEqual(self.uav.destination,item.destination)


    def test_deliver_item(self):
        # Prerequisites
        item = Item(destination=(0,0))
        self.uav.pick_up_item(item)

        # Test: dliver item, result: real_walk = [], number_of_delivered_items = 1, uav.destination != item.destination, state =3,
        # cargo_bay.item = None, item not in grid anymore
        self.uav.deliver_item()
        self.assertEqual(self.uav.real_walk,[])
        self.assertEqual(self.model.number_of_delivered_items,1)
        self.assertIsNot(self.uav.destination,item.destination)
        self.assertEqual(self.uav.state,3)
        self.assertIsNone(self.uav.cargo_bay.item)
        self.assertNotIn(item, self.uav.perceived_world_grid.get_cell_list_contents(item.destination))


    def test_check_battery(self):

        # 1st test: 0 < current_charge < battery_low, state != 5, result: state = 1,
        self.uav.state = 1
        self.uav.check_battery()
        self.assertEqual(self.uav.state,1)

        # 2nd Test: battery = max_charge, state = 5, cargo_bay empty, result: state = 1
        self.uav.state = 5
        self.uav.check_battery()
        self.assertEqual(self.uav.state,1)

        # 3rd Test: battery = max_charge, state = 5, cargo_bay not empty, result: state = 2, self.destination = cargo_bay.destination
        item = Item(destination=(0,0))
        self.uav.pick_up_item(item)
        self.uav.state = 5

        self.uav.check_battery()
        self.assertEqual(self.uav.state,2)
        self.assertEqual(self.uav.destination,self.uav.cargo_bay.get_destination())
        self.assertEqual(self.uav.destination,item.destination)

        # 4th Test: battery < battery_low, state != 5, result: state = 4, destination != item.destination
        self.uav.state = 2
        self.uav.battery._current_charge = 5
        self.uav.check_battery()

        self.assertEqual(self.uav.state,4)
        self.assertNotEqual(self.uav.destination,item.destination)

        # 4th Test: battery = 0, state != 5, result: state = 6
        self.uav.battery._current_charge = 0
        self.uav.check_battery()
        self.assertEqual(self.uav.state,6)

    def test_arrive_at_base_station(self):
        self.uav.state = 7
        # 1st Test: idle = True, charge = False
        self.uav.arrive_at_base_station(idle=True,charge=False)
        self.assertEqual(self.uav.state,1)

        # 2nd Test: idle = False, charge = True
        self.uav.state = 7
        self.uav.arrive_at_base_station(idle=False,charge=True)
        self.assertEqual(self.uav.state, 5)

        # 3rd Test: idle = charge = True
        self.uav.state = 7
        self.uav.arrive_at_base_station(idle=True,charge=True)
        self.assertEqual(self.uav.state,1)

        # 4th Test: idle = charge = False
        self.uav.state = 7
        self.uav.arrive_at_base_station(idle=False, charge= False)
        self.assertEqual(self.uav.state,7)

    def test_find_uavs_close(self):
        print("NOT YET DEFINED")
        self.assertTrue(True)



