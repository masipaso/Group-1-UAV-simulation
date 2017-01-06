import unittest
from delivery.grid.multi_grids import TwoMultiGrid
from delivery.agents.repellent import Repellent
from delivery.model.worldmodel import WorldModel

class TwoMultiGrid_test(unittest.TestCase):
    def setUp(self):
        self.grid = TwoMultiGrid(width=100, height=100,torus=False)


    def test_move_agent(self):
        agent = Repellent(model=WorldModel(),pos=(30,30))
        self.grid.place_agent(agent,(30,30))

        # 1st Test: Move agent out of grid, IndexError expected
        with self.assertRaises(IndexError):
            self.grid.move_agent(agent,(101,101))

        # 2nd Test: Move agent to a valid pos in grid
        self.grid = TwoMultiGrid(width=100, height=100, torus=False)
        self.grid.place_agent(agent, (30, 30))
        self.grid.move_agent(agent,(29,29))

        # Test: Is previous cell empty? Is agent in new cell?
        self.assertTrue(self.grid.is_cell_empty((30,30)))
        self.assertTrue(agent in self.grid.get_cell_list_contents((29,29)))

        # 3rd Test: Move agent to same position
        self.grid = TwoMultiGrid(width=100, height=100, torus=False)
        self.grid.place_agent(agent, (30, 30))
        self.grid.move_agent(agent,(30,30))
        self.assertTrue(agent in self.grid.get_cell_list_contents((30,30)))

    def test_get_repellent_on(self):

        # 1st Test: Check if get_repellent returns None when there is no repellent
        self.assertEqual(self.grid.get_repellent_on((30,30)),None)

        # 2nd Test: Place one repellent in a cell and test if it is a repellent
        agent = Repellent(model=WorldModel(), pos=(30, 30))
        self.grid.place_agent(agent,agent.pos)
        self.assertIsInstance(self.grid.get_repellent_on((30,30)),Repellent)
        self.assertIs(self.grid.get_repellent_on((30, 30)), agent)


