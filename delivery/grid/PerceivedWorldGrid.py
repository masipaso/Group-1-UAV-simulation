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

    def is_valid_altitude(self, pos_z):
        """
        Checks if the given altitude is valid
        :param pos_z: The altitude to check for
        :return: True, if the altitude is valid. Otherwise, False
        """
        # perceived_world is 0-index
        pos_z -= 1
        return True if 0 <= pos_z < len(self.perceived_world) else False

    def get_max_altitude(self):
        """
        Get the maximal altitude.
        :return: The maximal altitude
        """
        return len(self.perceived_world)

    def place_obstacle_at(self, pos):
        """
        Place an Obstacle at a given position
        :param pos: Triple of coordinates of the Obstacle
        """
        pos_x, pos_y, pos_z = pos
        # perceived_world is 0-index
        pos_z -= 1
        if 0 <= pos_z < len(self.perceived_world):
            self.perceived_world[pos_z][(pos_x, pos_y)] = self.OBSTACLE

    def place_empty_at(self, pos):
        """
        Place an "Empty" at a given position and altitude
        :param pos: Triple of coordinates of the "Empty"
        """
        pos_x, pos_y, pos_z = pos
        # perceived_world is 0-index
        pos_z -= 1
        if 0 <= pos_z < len(self.perceived_world):
            self.perceived_world[pos_z][(pos_x, pos_y)] = self.EMPTY

    def is_obstacle_at(self, pos):
        """
        Check if there is an Obstacle on the position
        !! Important: False is returned if the pos is unknown or the altitude is to high/low
        :param pos: Triple of coordinates
        :return: True, if there is an Obstacle. Otherwise, False
        """
        pos_x, pos_y, pos_z = pos
        # perceived_world is 0-index
        pos_z -= 1
        if 0 <= pos_z < len(self.perceived_world):
            if (pos_x, pos_y) in self.perceived_world[pos_z]:
                return True if math.isclose(self.perceived_world[pos_z][(pos_x, pos_y)], self.OBSTACLE, rel_tol=1e-5) else False
        return False

    def is_known(self, pos):
        """
        Check if the coordinates are known
        :param pos: Triple of coordinates
        :return: True, if there is information for this pos
        """
        pos_x, pos_y, pos_z = pos
        # perceived_world is 0-index
        pos_z -= 1
        if pos_z <= len(self.perceived_world):
            return True if (pos_x, pos_y) in self.perceived_world[pos_z] else False

    def get_known_coordinates_at(self, pos_z):
        """
        Return all known coordinates for a certain altitude
        :param pos_z: The altitude in question
        :return: A dictionary of all known coordinates at that altitude
        """
        # perceived_world is 0-index
        pos_z -= 1
        if pos_z <= len(self.perceived_world):
            return self.perceived_world[pos_z]