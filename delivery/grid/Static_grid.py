import configparser
import numpy as np
import math


class StaticGrid:
    """
    A StaticGrid is a Grid which contains simple, numeric information that doesnt change once it was initialized
    """
    def __init__(self, width, height, pixel_ratio, landscape):
        """
        Create a new StaticGrid
        :param width: The width of the grid
        :param height: The height of the grid
        :param pixel_ratio:
        :param landscape: A loaded Image file which has only two colors (black and white).
                        Black are obstacles and white is nothing.
        """
        # Constants
        self.BASE_STATION = -1
        self.OBSTACLE_DEFAULT = 1
        self.EMPTY = 0

        self.height = height
        self.width = width
        self.pixel_ratio = pixel_ratio
        self.landscape = landscape

        # Read config.cfg
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.max_altitude = config.getint('Grid', 'max_altitude')

        # Initialize an empty grid
        self.grid = np.zeros(shape=[self.width, self.height])

    def populate_grid(self):
        """
        Parse the landscape and populate the grid with the parsed information.
        Whenever there is a black pixel, create an Obstacle at the position
        """
        multiplier = max(round(self.pixel_ratio / 2), 1)

        # Read landscape to get locations of obstacles
        for j in range(1, self.height, multiplier):
            for i in range(1, self.width, multiplier):
                r, g, b = self.landscape[i, j]
                if self.is_obstacle_color(r, g, b):
                    fill_cells_x = []
                    fill_cells_y = []
                    for k in range(0, multiplier):
                        fill_cells_x.append(i - k)
                        fill_cells_y.append(self.height - j - k)

                    for x in fill_cells_x:
                        if 0 < x < self.width:
                            for y in fill_cells_y:
                                if 0 < y < self.height:
                                    self.place_obstacle((x, y))
                                else:
                                    break

    def get_neighborhood(self, pos, include_center=False, radius=1):
        """
        Return a list of cells that are in the neighborhood of a certain point.
        :param pos: Coordinate tuple for the neighborhood to get
        :param include_center: If True, return the (x, y) cell as well.
                               Otherwise, return only the surrounding cells.
        :param radius: Radius of cells to get.
        :return: A list of coordinate tuples representing the neighborhood.
        """
        x, y = pos
        neighborhood = set()

        # Add neighboring coordinates until the desired radius is reached
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dy is 0 and dx is 0 and not include_center:
                    continue

                # Calculate new coordinates
                px = x + dx
                py = y + dy
                coordinates = (px, py)

                # Check if the new coordinates are out of bounds
                if self.out_of_bounds(coordinates):
                    # ... and skip if this is the case
                    continue

                # Check if the coordinates are already in the list of neighborhood
                if coordinates not in neighborhood:
                    neighborhood.add(coordinates)

        return list(neighborhood)

    def out_of_bounds(self, pos):
        """
        Check if a position is out of bounds of the grid.
        :param pos: Tuple of coordinates to check.
        :return: True, if the position is out of bounds. Otherwise, False.
        """
        x, y = pos
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def place_obstacle(self, pos, altitude=1):
        """
        Place an obstacle at the given position
        :param pos: Tuple of coordinates
        :param altitude: Altitude of the Obstacle
        """
        if altitude < 1 or altitude > self.max_altitude:
            return
        self._place_agent(pos, self.OBSTACLE_DEFAULT * altitude)

    def place_base_station(self, pos):
        """
        Place an obstacle at the given position
        :param pos: Tuple of coordinates
        """
        self._place_agent(pos, self.BASE_STATION)

    def _place_agent(self, pos, type):
        """
        Place a specific type of obstacle at the given position
        :param pos: Tuple of coordinates
        :param type: 1 = Obstacle, 2 = BaseStation
        """
        x, y = pos
        self.grid[x][y] = type

    def is_cell_empty(self, pos):
        """
        Checks if a cell is empty
        :param pos: Tuple of coordinates
        :return: True if the cell is empty. Otherwise, False
        """
        x, y = pos
        return True if math.isclose(self.grid[x, y], self.EMPTY, rel_tol=1e-5) else False

    def is_obstacle_at(self, pos, altitude=1):
        """
        Checks if a cell contains an Obstacle
        :param pos: Tuple of coordinates
        :param altitude: Altitude to check for
        :return: True if the cell contains an Obstacle. Otherwise, False
        """
        x, y = pos
        return True if math.isclose(self.grid[x, y], self.OBSTACLE_DEFAULT * altitude, rel_tol=1e-5) else False

    def is_base_station_at(self, pos):
        """
        Checks if a cell contains a BaseStation
        :param pos: Tuple of coordinates
        :return: True if the cell contains a BaseStation. Otherwise, False
        """
        x, y = pos
        return True if math.isclose(self.grid[x, y], self.BASE_STATION, rel_tol=1e-5) else False

    @staticmethod
    def is_obstacle_color(r, g, b):
        black = range(0, 240)
        return r in black and g in black and b in black
