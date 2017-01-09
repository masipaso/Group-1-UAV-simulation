import unittest
from delivery.agents.uav import Uav
from delivery.agents.item import Item
from delivery.agents.baseStation import BaseStation
from delivery.model.worldmodel import WorldModel

class UAV_test(unittest.TestCase):

    def setUp(self):
        self.model = WorldModel()
        self.baseStation = BaseStation(model=self.model, pos=(200, 200), id=1, center=(200, 200), range_of_base_station=250)
        self.uav = Uav(model=self.model, pos=(200,200),id=1,max_battery=1000,battery_low=20,base_station=self.baseStation)

    def test_init(self):
        self.assertEqual(self.uav.model,self.model)
        self.assertEqual(self.uav.pos,(200,200))
        self.assertEqual(self.uav.id,1)
        self.assertEqual(self.uav.max_battery,1000)
        self.assertEqual(self.uav.battery_low,20)
        self.assertEqual(self.uav.base_station,self.baseStation)

    def test_pickup_item(self):
        # Set state of UAV to 4, so no item should be picked up
        item = Item(destination=(50, 50))


        # Test negative cases: at state = 2..6 no item should be picked up and state should be unchanged
        for i in range(2,6,1):
            self.uav.state = i
            self.uav.pick_up_item(item)

            # Test if state unchanged after pick_up_item(item)
            self.assertEqual(self.uav.state, i)

            # Test if item was not picked up
            self.assertEqual(self.uav.item, None)

        # Positive case: state = 1, item should be picked up and state be changed to 2
        self.uav.state = 1
        self.uav.pick_up_item(item)

        # Test if state == 2 after pick_up_item(item)
        self.assertEqual(self.uav.state,2)

        # Test if len(walk) == 0 after pick_up_item(item
        self.assertEqual(len(self.uav.walk),0)

        # Test if item was picked up
        self.assertEqual(self.uav.item,item)

    def test_deliver_item(self):
        # Prerequisites
        self.baseStation.create_item()
        self.uav.state = 1
        self.uav.pick_up_item(self.baseStation.get_item())
        # Creating a short fake walk to test if it is cleared after delivery
        self.uav.walk = [(50,49),(49,49)]
        self.uav.real_walk = self.uav.walk
        self.uav.pos = (50,50)

        # Run deliver item
        self.uav.deliver_item()

        # Test if item has been cleared
        self.assertEqual(self.uav.item, None)

        # Tests if walk and real_walk are cleared
        self.assertEqual(self.uav.walk, [])
        self.assertEqual(self.uav.real_walk,[])

        # Test if new destination is baseStation
        self.assertEqual(self.uav.destination,self.baseStation.pos)

        # Test if state has changed to 3
        self.assertEqual(self.uav.state,3)

    def test_check_battery(self):

        # 1st test: 0 < current_charge < battery_low
        self.uav.destination = (50, 50)
        self.uav.state = 1
        self.uav.current_charge = self.uav.battery_low - 1
        self.uav.check_battery()

        # Test if state is changed to 4
        self.assertEqual(self.uav.state,4)

        # Test if UAV's destination is self.baseStation.pos
        self.assertEqual(self.uav.destination,self.baseStation.pos)

        # 2nd test: 0 = current_charge
        self.uav.destination = (50, 50)
        self.uav.state = 1
        self.uav.current_charge = 0
        self.uav.check_battery()

        # Test if UAV's state is changed to 6
        self.assertEqual(self.uav.state, 6)

        # Test if UAV's destination is changed
        self.assertEqual(self.uav.destination,self.baseStation.pos)


        # 3rd test: 0 > current_charge
        self.uav.destination = (50, 50)
        self.uav.state = 1
        self.uav.current_charge = -1
        self.uav.check_battery()

        # Test if UAV's state is changed to 6
        self.assertEqual(self.uav.state, 6)

        # Test if UAV's destination is changed
        self.assertEqual(self.uav.destination,self.baseStation.pos)

        # 4th Test: 0 < current_charge > low_battery
        self.uav.destination = (50, 50)
        self.uav.state = 1
        self.uav.current_charge = self.uav.max_battery
        self.uav.check_battery()

        # Test if UAV's state is unchanged
        self.assertEqual(self.uav.state, 1)

        # Test if UAV's destination is changed
        self.assertEqual(self.uav.destination,(50,50))

    def test_charge_battery(self):

        # 1st Test: current_charge < max_charge and carrying an item
        self.uav.item = Item(destination=(50,50))
        self.uav.current_charge = 0.7 * self.uav.current_charge
        self.uav.charge_battery()

        # Test if battery has been charged
        self.assertGreater(self.uav.current_charge,0.7* self.uav.current_charge)

        # 2nd Test: current_charge = max_charge and no item carried
        self.uav.state = 7
        self.uav.item = None
        self.uav.current_charge = self.uav.max_battery
        self.uav.charge_battery()

        # Test if current_charge = max_charge
        self.assertEqual(self.uav.current_charge,self.uav.max_battery)

        # Test if state changed to 1
        self.assertEqual(self.uav.state,1)

        # 3rd Test: Battery fully charged, carrying an item
        self.uav.state = 7
        item = Item(destination=(50,50))
        self.uav.item = item
        self.uav.current_charge = self.uav.max_battery
        self.uav.charge_battery()

        # Test if state changed to 2
        self.assertEqual(self.uav.state,2)

        # Test if destination = item.destination
        self.assertEqual(self.uav.destination,item.destination)

        # Test if current_charge = max_charge
        self.assertEqual(self.uav.current_charge,self.uav.max_battery)

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

    def test_move_to(self):
        self.model.grid.place_agent(self.uav, self.uav.pos)
        self.model.perceived_world_grid.place_agent(self.uav, self.uav.pos)
        self.uav.move_to((40,40))

        self.assertEqual(self.uav.pos,(40,40))


    def test_get_euclidean_distance(self):

        # 1st Test: Distance = 1
        pos1 = (40,40)
        pos2 = (41,40)
        distance = 1
        computed_distance = self.uav.get_euclidean_distance(pos1,pos2)
        self.assertEqual(computed_distance,distance)

        # 2nd Test: Distance = 10, x changed
        pos1 = (40,40)
        pos2 = (50,40)
        distance = 10
        computed_distance = self.uav.get_euclidean_distance(pos1,pos2)
        self.assertEqual(computed_distance,distance)

        # 3rd Test: Distance = 10, y changed
        pos1 = (40,40)
        pos2 = (40,50)
        distance = 10
        computed_distance = self.uav.get_euclidean_distance(pos1,pos2)
        self.assertEqual(computed_distance,distance)

        # 3rd Test: Distance = 14.142135623730951, x,y changed
        pos1 = (40,40)
        pos2 = (30,30)
        distance = 14.142135623730951
        computed_distance = self.uav.get_euclidean_distance(pos1,pos2)
        self.assertEqual(computed_distance,distance)

    def test_get_grid(self):
        self.assertEqual(self.uav.get_grid(self),self.uav.grid)

    def test_test_find_uavs_close(self):
        print("NOT YET DEFINED")
        self.assertTrue(True)