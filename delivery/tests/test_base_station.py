import unittest
from delivery.agents.BaseStation import BaseStation
from delivery.agents.Item import Item
from delivery.model.Worldmodel import WorldModel


class BaseStationTest(unittest.TestCase):
    def setUp(self):
        self.model = WorldModel()
        self.baseStation = BaseStation(model=self.model, pos=(2, 2, 2), bid=1, center=(2, 2), range_of_base_station=250)

    def test_init(self):
        self.assertEqual(self.baseStation.model, self.model)
        self.assertEqual(self.baseStation.pos, (2, 2, 2))
        self.assertEqual(self.baseStation.bid, 1)
        self.assertEqual(self.baseStation.center, (2, 2))
        self.assertEqual(self.baseStation.range_of_base_station, 250)

    def test_step(self):
        # 1st Test: No items at BaseStation, Result: len(basestation.items) = 1
        self.baseStation.step()
        self.assertEqual(len(self.baseStation.items), 1)

        # 2nd Test: max_items_per_base_station = 1, 1 items at BaseStation. Result after: 1 item at BaseStation
        self.baseStation.max_items_per_base_station = 1
        self.baseStation.step()
        self.assertEqual(len(self.baseStation.items), 1)

    def test_create_item(self):
        # Creating one item and checking if it was created
        self.assertEquals(len(self.baseStation.items), 0)
        self.baseStation.create_item()
        self.assertEquals(len(self.baseStation.items), 1)

        # Getting the item from the list of items (can only be the one just created because we checked if the list was empty first)
        item = self.baseStation.items.pop(0)

        # Check if item is on perceived_world_grid at its destination position
        self.assertIn(member=item, container=self.model.item_schedule.agents)

    def test_get_item(self):
        # 1st Test: no items at baseStation. Expected Result: None
        self.assertIsNone(self.baseStation.get_item())

        # 2nd Test. 4 items at BaseStation.
        # Creating some items
        self.baseStation.create_item()
        self.baseStation.create_item()
        self.baseStation.create_item()
        self.baseStation.create_item()

        # Expected result: get_item is Not None, len(items) has decreased to exactly 3
        self.assertIsNotNone(self.baseStation.get_item())
        self.assertEqual(len(self.baseStation.items), 3)

        # Testing it picked_up_items has been increased to exactly one
        self.assertEqual(self.baseStation.picked_up_items, 1)

    def test_get_number_of_items(self):
        # Creating some items
        self.baseStation.create_item()
        self.baseStation.create_item()
        self.baseStation.create_item()
        self.baseStation.create_item()
        item_count = 4

        # Testing if method returns correct item count for items that have not been picked up
        self.assertEqual(self.baseStation.get_number_of_items(picked_up=False), item_count)

        self.baseStation.get_item()
        self.baseStation.get_item()
        picked_up_item_count = 2
        item_count = 2

        # Testing if method returns correct item count for items that have not been picked up after 2 have been picked up
        self.assertEqual(self.baseStation.get_number_of_items(picked_up=False), item_count)

        # Testing if method returns correct item count for items that have been picked up
        self.assertEqual(self.baseStation.get_number_of_items(picked_up=True), picked_up_item_count)

    def test_sort_items_by_priority(self):
        self.baseStation.items.append(Item(destination=(10, 10), priority=3, iid=2))
        self.baseStation.items.append(Item(destination=(10, 10), priority=4, iid=3))
        self.baseStation.items.append(Item(destination=(10, 10), priority=6, iid=4))
        self.baseStation.items.append(Item(destination=(10, 10), priority=1, iid=1))

        self.baseStation.sort_items_by_priority()

        i = 0
        while not len(self.baseStation.items) == 0:
            item = self.baseStation.items.pop(0)
            i += 1
            self.assertEqual(item.iid, i)

    def test_get_pos(self):
        self.assertEqual(self.baseStation.get_pos(), self.baseStation.pos)
