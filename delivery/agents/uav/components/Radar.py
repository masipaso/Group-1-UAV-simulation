class Radar:
    """
    The Radar of an UAV
    """
    # TODO: More details

    def __init__(self, landscape, coverage_range):
        """
        Initialize the Radar
        :param landscape: The landscape of the model
        :param coverage_range: The range the Radar can cover
        """
        self.landscape = landscape
        self.coverage_range = coverage_range

    def is_obstacle_at(self, pos, altitude=1):
        """
        Scan the landscape and check if there is an Obstacle at the given position
        :param pos: Tuple of coordinates to check
        :param altitude: Altitude to check for
        :return: True if there is an Obstacle, otherwise False
        """
        return self.landscape.is_obstacle_at(pos, altitude)

    def is_base_station_at(self, pos):
        """
        Scan the landscape and check if there is an BaseStation at the given position
        :param pos: Tuple of coordinates to check
        :return: True if there is an BaseStation, otherwise False
        """
        return self.landscape.is_base_station_at(pos)

    def scan_neighborhood(self, pos):
        """
        Scan the neighborhood around a given position
        :param pos: Tuple of coordinates
        :return: All the neighboring cells in the radius of the coverage_range around the pos
        """
        return self.landscape.get_neighborhood(pos, self.coverage_range)
