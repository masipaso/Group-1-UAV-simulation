import sys
import unittest
import configparser
from delivery.grid.StaticGrid import StaticGrid
from PIL import Image


class StaticGridTest(unittest.TestCase):

    def setUp(self):
        # Read landscape
        config = configparser.ConfigParser()
        config.read('./config.ini')

        try:
            self.width = config.getint('Grid', 'width', fallback=500)
        except ValueError:
            print("[Configuration] The range_of_base_station is not valid.")
            sys.exit(1)

        try:
            self.height = config.getint('Grid', 'height', fallback=500)
        except ValueError:
            print("[Configuration] The range_of_base_station is not valid.")
            sys.exit(1)

        try:
            self.pixel_ratio = config.getint('Grid', 'pixel_ratio', fallback=10)
        except ValueError:
            print("[Configuration] The range_of_base_station is not valid.")
            sys.exit(1)

        background_image_source = config.get('Grid', 'image',
                                             fallback='./delivery/visualization/images/a_city500x500.jpg')
        if type(background_image_source) is not str:
            print("[Configuration] The image is not valid.")
            sys.exit(1)

        background_image = Image.open(background_image_source)
        self.background = background_image.load()
        self.grid = StaticGrid(self.width, self.height, self.background)

    def test_init(self):
        self.assertEqual(self.grid.width,self.width)
        self.assertEqual(self.grid.height,self.height)
        self.assertEqual(self.grid.landscape,self.background)
        self.assertEqual(self.grid.BASE_STATION,-1)
        self.assertEqual(self.grid.OBSTACLE_DEFAULT,1)
        self.assertEqual(self.grid.EMPTY,0)
        self.assertIsNotNone(self.grid.grid)

    def test_get_neighborhood(self):
        # 1st Test: Default values for method: include_center = False, radius = 1 return same value as not specifying them
        neighborhood = self.grid.get_neighborhood(pos=(10, 10), include_center=False, radius=1)
        neighborhood_notspecified = self.grid.get_neighborhood(pos=(10, 10))

        # Both objects should be equal and (10,10) (center) not in the list
        self.assertEqual(neighborhood, neighborhood_notspecified)
        self.assertNotIn((10, 10), neighborhood)

        # 2nd Test: neighborhood should contain 8 fields
        self.assertEqual(len(neighborhood), 8)

        # 3rd Test: invalid fields not in output of function get_neighborhood
        neighborhood = self.grid.get_neighborhood(pos=(0, 0), include_center=False, radius=1)

        self.assertNotIn((-1, 0), neighborhood)
        self.assertGreater(8, len(neighborhood))

        # 4th Test: center is in neighborhood
        neighborhood = self.grid.get_neighborhood(pos=(0, 0), include_center=True, radius=1)
        self.assertIn((0, 0), neighborhood)

    def test_out_of_bounds(self):
        # 1st Test: Valid position: 0 <= x < width, 0 <= y < height. Expected result: False
        self.assertFalse(self.grid.is_out_of_bounds((self.width - 1, self.height - 1)))

        # 2nd Test: Invalid position: -1 = x, 0 <= y < height. Expected result: True
        self.assertTrue(self.grid.is_out_of_bounds((-1, self.height - 1)))

        # 3rd Test: Invalid position: 0 <= x < width, -1 = y. Expected result: True
        self.assertTrue(self.grid.is_out_of_bounds((self.width - 1, -1)))

        # 4th Test: Invalid position: -1 = x = y. Expected Result: True
        self.assertTrue(self.grid.is_out_of_bounds((-1, -1)))

        # 5th Test: Invalid position:  x >= width, 0 <= y <= height. Expected Result: True
        self.assertTrue(self.grid.is_out_of_bounds((self.width + 1, self.height - 1)))

        # 6th Test: Invalid position:  0 <= x < height, y >= height. Expected Result: True
        self.assertTrue(self.grid.is_out_of_bounds((self.width - 1, self.height + 1)))

        # 7th Test: Invalid position: x = width+1, y = height + 1
        self.assertTrue(self.grid.is_out_of_bounds((self.width + 1, self.height + 1)))

    def test_place_obstacle(self):
        self.grid.place_obstacle((1, 1))
        self.assertEqual(self.grid.grid[1, 1], 1)

    def test_place_base_station(self):
        self.grid.place_base_station((1, 1))
        self.assertEqual(self.grid.grid[1, 1], -1)

    def test_place_agent(self):
        # Test: After running the method with a pos=(x,y), the grid stored should have a float with type
        self.grid._place_agent((1, 1), 1)
        self.assertEqual(self.grid.grid[1, 1], 1)

    def test_is_cell_empty(self):
        # 1st Test: Empty field. Expected Result: True
        self.assertTrue(self.grid.is_cell_empty((10, 10)))

        # 2nd Test: Place agent on a field. Expected Result: False
        self.grid._place_agent((10, 10), 1)
        self.assertFalse(self.grid.is_cell_empty((10, 10)))

    def test_is_obstacle_at(self):
        # 1st Test: Empty field. Expected Result: False
        self.assertFalse(self.grid.is_obstacle_at((10, 10)))

        # 2nd Test: Obstacle at field. Expected Result: True
        self.grid._place_agent((10, 10), 1)
        self.assertTrue(self.grid.is_obstacle_at((10, 10)))

    def test_is_base_station_at(self):
        # 1st Test: Empty field. Expected Result: False
        self.assertFalse(self.grid.is_base_station_at((10, 10)))

        # 2nd Test: Obstacle at field. Expected Result: True
        self.grid._place_agent((10, 10), -1)
        self.assertTrue(self.grid.is_base_station_at((10, 10)))

        # 3rd Test: Other type at field. Expected Result: False
        self.grid._place_agent((10, 11), 1)
        self.assertFalse(self.grid.is_base_station_at((10, 11)))
