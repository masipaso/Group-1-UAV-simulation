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
