class PerceivedWorldGrid():
    """
    A PerceivedWorldGrid is actually not a real grid. It is a list of dictionaries containing grid-like information
    about the perceived world, i.e. information about Repellents.
    """

    def __init__(self, max_altitude):
        """
        Create a new PerceivedWorldGrid
        :param max_altitude: The maximum altitude of the grid (= number of dictionaries)
        """
        self.max_altitude = max_altitude
        self.perceived_world = []
        for altitude in range(1, max_altitude):
            self.perceived_world.append(dict())

    def place_repellent_at(self, repellent, pos, altitude=1):
        """
        Place a Repellent at a given position and altitude
        :param repellent: The Repellent that is located
        :param pos: Tuple of coordinates
        :param altitude: The altitude of the Repellent
        """
        # perceived_world is 0-index
        altitude -= 1
        if altitude > self.max_altitude:
            return
        self.perceived_world[altitude][pos] = repellent

    def get_repellent_on(self, pos, altitude=1):
        """
        Get the Repellent on the position
        :param pos: Tuple of coordinates
        :param altitude: The altitude to check for
        :return: A repellent, that is on the position or None
        """
        # perceived_world is 0-index
        altitude -= 1
        if altitude <= len(self.perceived_world):
            if pos in self.perceived_world[altitude]:
                return self.perceived_world[altitude][pos]
        return None

    def get_repellents_on(self, altitude=1):
        """
        Get all Repellents on a certain altitude
        :param altitude: The altitude to check for
        :return: A dictionary of Repellents
        """
        # perceived_world is 0-index
        altitude -= 1
        if altitude <= len(self.perceived_world):
            return self.perceived_world[altitude]
        return None

    def has_repellents_on(self, altitude=1):
        """
        Check if there are Repellents on a certain altitude
        :param altitude: The altitude to check for
        :return: True if there are Repellents on that altitude
        """
        # perceived_world is 0-index
        altitude -= 1
        if altitude <= len(self.perceived_world):
            return True if len(self.perceived_world[altitude]) > 0 else False
        return False

    def remove_repellent(self, pos, altitude):
        """
        Remove a Repellent
        :param pos: Tuple of coordinates
        :param altitude: Altitude of the Repellent
        """
        # perceived_world is 0-index
        altitude -= 1
        if altitude <= len(self.perceived_world):
            self.perceived_world[altitude].pop(pos)