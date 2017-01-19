from delivery.agents.BaseStation import BaseStation


class Sensor:
    """
    The Sensor of an UAV
    """
    # TODO: More details

    def __init__(self, grid, landscape, coverage_range):
        """
        Initialize the Sensor
        :param grid: The grid of the model
        :param landscape: The landscape of the model
        :param coverage_range: The range the Sensor can cover
        """
        self.grid = grid
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

    def scan_for_uavs(self, pos):
        """
        Scan for UAVs in the neighborhood
        :param pos: Tuple of coordinates
        :return: A list of UAVs that are close to the pos
        """
        other_uavs = []
        neighborhood = self.grid.get_neighborhood(pos=pos, moore=True, include_center=False, radius=self.coverage_range)
        for cell in neighborhood:
            for obj in self.grid.get_cell_list_contents(cell):
                # Check if the obj is NOT a BaseStation
                if type(obj) is not BaseStation:
                    other_uavs.append(obj)
        return other_uavs
