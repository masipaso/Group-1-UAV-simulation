import math


class PerceivedWorldGrid:
    """
    A PerceivedWorldGrid is actually not a real grid. It is a list of dictionaries containing grid-like information
    about the perceived world, i.e. information about Repellents.
    """

    def __init__(self, max_altitude):
        """
        Create a new PerceivedWorldGrid
        :param max_altitude: The maximum altitude of the grid (= number of dictionaries)
        """
        # Constants
        self.OBSTACLE = 1
        self.EMPTY = 0

        self.max_altitude = max_altitude
        self.perceived_world = []
        for altitude in range(0, max_altitude):
            self.perceived_world.append(dict())

    def place_obstacle_at(self, pos, altitude=1):
        # perceived_world is 0-index
        altitude -= 1
        if 0 <= altitude < len(self.perceived_world):
            self.perceived_world[altitude][pos] = self.OBSTACLE
        return

    def is_obstacle_at(self, pos, altitude=1):
        """
        Check if there is an Obstacle on the position
        !! Important: False is returned if the pos is unknown or the altitude is to high/low
        :param pos: Tuple of coordinates
        :param altitude: The altitude to check for
        :return: True, if there is an Obstacle. Otherwise, False
        """
        # perceived_world is 0-index
        altitude -= 1
        if 0 <= altitude < len(self.perceived_world):
            if pos in self.perceived_world[altitude]:
                return True if math.isclose(self.perceived_world[altitude][pos], self.OBSTACLE, rel_tol=1e-5) else False
        return False

    def is_known(self, pos, altitude):
        """
        Return all known coordinates for a certain altitude
        :param pos: Tuple of coordinates
        :param altitude: The altitude in question
        :return: True, if there is information for this pos
        """
        altitude -= 1
        if altitude <= len(self.perceived_world):
            return True if pos in self.perceived_world[altitude] else False

    def place_empty_at(self, pos, altitude=1):
        # perceived_world is 0-index
        altitude -= 1
        if 0 <= altitude < len(self.perceived_world):
            self.perceived_world[altitude][pos] = self.EMPTY
        return

    def get_known_coordinates_at(self, altitude):
        """
        Return all known coordinates for a certain altitude
        :param altitude: The altitude in question
        :return: A dictionary of all known coordinates at that altitude
        """
        altitude -= 1
        if altitude <= len(self.perceived_world):
            return self.perceived_world[altitude]