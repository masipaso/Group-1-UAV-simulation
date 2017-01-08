import unittest
from delivery.agents.item  import Item
from mesa.space import MultiGrid

class Item_test(unittest.TestCase):
    def setUp(self):
        self.item = Item(destination=(10,10),priority=1,id=0)


    def test_deliver(self):
        # Test if after deliver() the item is removed from the grid
        grid = MultiGrid(width=100,height=100,torus=False)
        grid._place_agent((10,10),self.item)

        self.item.deliver(grid=grid)

        self.assertNotIn(self.item,grid.get_cell_list_contents((10,10)))

    def test_get_destination(self):
        # Test if this method returns the correct destination
        self.assertEqual(self.item.destination,self.item.get_destination())

