import unittest
from delivery.agents.baseStation import BaseStation
from delivery.model.worldmodel import WorldModel

class baseStationTest(unittest.TestCase):
    def setUp(self):
        self.model = WorldModel()
        self.baseStation = BaseStation(model=self.model, pos=(2, 2), id=1, center=(2, 2), range_of_base_station=250)

    def test_create_item(self):

        #Think of more cases for the method

        #Creating one item and checking if it was created
        self.assertEquals(len(self.baseStation.items),0)
        self.baseStation.create_item()
        self.assertEquals(len(self.baseStation.items),1)


    def test_get_item(self):
        #Think of more cases for the method

        #Creating some items
        self.baseStation.create_item()
        self.baseStation.create_item()
        self.baseStation.create_item()
        self.baseStation.create_item()

        item_count = len(self.baseStation.items)

        self.baseStation.get_item()
        self.assertGreater(item_count,len(self.baseStation.items))

        # Testing it picked_up_items has been increased to exactly one
        self.assertEqual(self.baseStation.picked_up_items,1)


    def test_get_number_of_items(self):
        #Creating some items
        self.baseStation.create_item()
        self.baseStation.create_item()
        self.baseStation.create_item()
        self.baseStation.create_item()
        item_count = 4

        # Testing if method returns correct item count for items that have not been picked up
        self.assertEqual(self.baseStation.get_number_of_items(picked_up=False),item_count)

        self.baseStation.get_item()
        self.baseStation.get_item()
        pickedup_item_count = 2
        item_count = 2

        # Testing if method returns correct item count for items that have not been picked up after 2 have been picked up
        self.assertEqual(self.baseStation.get_number_of_items(picked_up=False), item_count)

        # Testing if method returns correct item count for items that have been picked up
        self.assertEqual(self.baseStation.get_number_of_items(picked_up=True), pickedup_item_count)




