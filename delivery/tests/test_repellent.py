import unittest
from delivery.agents.repellent import Repellent
from delivery.model.worldmodel import WorldModel
from mesa.space import MultiGrid
import configparser

class repellent_Test(unittest.TestCase):

    def setUp(self):
        self.model = WorldModel()
        self.grid = MultiGrid(width=100, height=100, torus=False)
        self.repellent = Repellent(model=self.model,pos=(30,30),grid=self.grid)

        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.initialStrength = config.getfloat('Repellent', 'initial_strength')
        self.decreaseBy = config.getfloat('Repellent', 'decrease_by')

    def test_init(self):
        self.assertEqual(self.repellent.decrease_by, self.decreaseBy)
        self.assertEqual(self.repellent.initial_strength, self.initialStrength)
        self.assertEqual(self.repellent.model,self.model)
        self.assertEqual(self.repellent.pos,(30,30))
        self.assertIn(self.repellent,self.model.repellent_schedule.agents)

    def test_step(self):
        # Prerequisites: placing repellent on grid and add to scheduler
        self.grid.place_agent(self.repellent,self.repellent.pos)
        self.model.repellent_schedule.add(self.repellent)

        # 1st Test: strength > 0 = initial_strength. Expected result: strength = initial_strength - decrease_by and repellent not removed from scheduler and grid
        self.repellent.step()
        self.assertEqual(self.repellent.strength,self.initialStrength-self.decreaseBy)

        found = False

        for elem in self.grid.get_cell_list_contents((30, 30)):
            if isinstance(elem, Repellent):
                found = True
                break

        self.assertTrue(found)

        self.assertIn(self.repellent, self.model.repellent_schedule.agents)

        # 2nd Test: strength = 0. Expected result: agent removed from schedule and grid, and strength = 0 -decrease_by
        self.repellent.strength = 0
        self.repellent.step()
        self.assertNotIn(self.repellent,self.repellent.grid)
        self.assertNotIn(self.repellent,self.model.repellent_schedule.agents)


    def test_strengthen(self):
        # Expected result: strength = initial_strength
        self.repellent.strength = 0
        self.repellent.strengthen()

        self.assertEqual(self.repellent.strength,self.initialStrength)

    def test_weaken(self):
        # Expected result: strength = initial_strength - decrease_by
        self.repellent.weaken()
        self.assertEqual(self.repellent.strength,self.initialStrength-self.decreaseBy)

    def test_get_position(self):
        # Expected result: get_position = repellent.pos = (30,30)
        pos = self.repellent.get_position()

        self.assertEqual(self.repellent.pos,pos)
        self.assertEqual((30,30),pos)

