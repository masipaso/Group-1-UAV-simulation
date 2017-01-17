import unittest
from delivery.agents.Item  import Item
from mesa.space import MultiGrid

class Item_Test(unittest.TestCase):
    def setUp(self):
        self.item = Item(destination=(10,10),priority=1,iid=0)

    def test_init(self):
        self.assertEqual(self.item.destination,(10,10))
        self.assertEqual(self.item.priority,1)
        self.assertEqual(self.item.iid,0)
        self.assertEqual(self.item.lifetime,0)
        self.assertFalse(self.item.delivered)

    def test_set_delivered(self):
        # Test if after deliver() the item is removed from the grid
        grid = MultiGrid(width=100,height=100,torus=False)
        grid._place_agent((10,10),self.item)

        self.item.set_delivered()

        self.assertTrue(self.item.delivered)

    def test_get_destination(self):
        # Test if this method returns the correct destination
        self.assertEqual(self.item.destination,self.item.get_destination())

    def test_step(self):
        # 1st Test: Run step and check if lifetime has increased
        self.item.step()
        self.assertEqual(self.item.lifetime,1)

        # 2nd Test: Item has been delivered. Lifetime should not have increased
        self.item.lifetime = 10
        self.item.delivered = True
        self.item.step()
        self.assertEqual(self.item.lifetime,10)

    def test_get_lifetime(self):
        # Test: Run get_lifetime and check if correct lifetime is returned
        # 1st Test: In the beginning get_lifetime = 0
        self.assertEqual(self.item.get_lifetime(),0)

        # 2nd Test: After 1 step, get_lifetime = 1
        self.item.step()
        self.assertEqual(self.item.get_lifetime(),1)
