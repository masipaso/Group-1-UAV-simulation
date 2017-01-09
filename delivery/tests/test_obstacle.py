import unittest
from delivery.agents.obstacle import Obstacle
from delivery.model.worldmodel import WorldModel


class Obstacle_Test(unittest.TestCase):

    def setUp(self):
        self.obstacle = Obstacle(model=None,pos=(10,10))

    def test_init(self):
        self.assertEqual(self.obstacle.pos,(10,10))

    def test_get_position(self):
        # Expect obstacle.pos = obstacle.get_position()
        self.assertEqual(self.obstacle.pos,(10,10))
        self.assertEqual(self.obstacle.pos,self.obstacle.get_position())