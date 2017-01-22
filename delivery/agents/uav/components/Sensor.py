from delivery.agents.BaseStation import BaseStation


class Sensor:
    """
    The Sensor of an UAV
    """
    # TODO: More details

    def __init__(self, grid, landscape, perceived_world, sensor_range):
        """
        Initialize the Sensor
        :param grid: The grid of the model (Actual world representation of UAVs)
        :param landscape: The landscape of the model (Actual world representation)
        :param perceived_world: The world as it is perceived by the UAV
        :param sensor_range: The range the Sensor can cover
        """
        self.grid = grid
        self.landscape = landscape
        self.perceived_world = perceived_world
        self.sensor_range = sensor_range

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

    def scan(self, pos, altitude):
        """
        Scan the neighborhood around a given position (of the real world), then store the new knowledge (perceived world).
        :param pos: Tuple of coordinates
        :param altitude: Current altitude of the UAV
        """
        neighborhood = self.landscape.get_neighborhood(pos, False, self.sensor_range)
        for coordinates in neighborhood:
            for temp_altitude in range(altitude - self.sensor_range, altitude + self.sensor_range):
                if self.is_obstacle_at(coordinates, temp_altitude):
                    self.perceived_world.place_obstacle_at(coordinates, temp_altitude)
                else:
                    self.perceived_world.place_empty_at(coordinates, temp_altitude)

    def scan_for_uavs(self, pos):
        """
        Scan for UAVs in the neighborhood
        :param pos: Tuple of coordinates
        :return: A list of UAVs that are close to the pos
        """
        other_uavs = []
        neighborhood = self.grid.get_neighborhood(pos=pos, moore=True, include_center=False, radius=self.sensor_range)
        for cell in neighborhood:
            for obj in self.grid.get_cell_list_contents(cell):
                # Check if the obj is NOT a BaseStation
                if type(obj) is not BaseStation:
                    other_uavs.append(obj)
        return other_uavs
