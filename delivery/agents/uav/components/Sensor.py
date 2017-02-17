from delivery.agents.BaseStation import BaseStation


class Sensor:
    """
    The Sensor of an UAV
    """

    def __init__(self, agents, landscape, perceived_world, sensor_range):
        """
        Initialize the Sensor
        :param agents: All the agents of the model (BaseStations and UAVs
        :param landscape: The landscape of the model (Actual world representation)
        :param perceived_world: The world as it is perceived by the UAV
        :param sensor_range: The range the Sensor can cover
        """
        self.agents = agents
        self.landscape = landscape
        self.perceived_world = perceived_world
        self.sensor_range = sensor_range

    def is_out_of_bounds(self, pos):
        """
        Scan the landscape and check if this is a valid position
        :param pos: Triple of coordinates to check
        :return: True, if the position is invalid. Otherwise, False.
        """
        pos_x, pos_y, pos_z = pos
        return self.landscape.is_out_of_bounds((pos_x, pos_y))

    def is_obstacle_at(self, pos):
        """
        Scan the landscape and check if there is an Obstacle at the given position
        :param pos: Triple of coordinates to check
        :return: True if there is an Obstacle, otherwise False
        """
        pos_x, pos_y, pos_z = pos
        return self.landscape.is_obstacle_at((pos_x, pos_y), pos_z)

    def is_base_station_at(self, pos):
        """
        Scan the landscape and check if there is an BaseStation at the given position
        :param pos: Triple of coordinates to check
        :return: True if there is an BaseStation, otherwise False
        """
        pos_x, pos_y, pos_z = pos
        return self.landscape.is_base_station_at((pos_x, pos_y), pos_z)

    def scan(self, pos):
        """
        Scan the neighborhood around a given position (of the real world), then store the new knowledge (perceived world).
        :param pos: Triple of coordinates
        """
        neighborhood = set()

        pos_x, pos_y, pos_z = pos

        # Add neighboring coordinates until the desired radius is reached
        for dy in range(-self.sensor_range, self.sensor_range + 1):
            for dx in range(-self.sensor_range, self.sensor_range + 1):
                for dz in range(-self.sensor_range, self.sensor_range + 1):
                    # Calculate new coordinates
                    px = pos_x + dx
                    py = pos_y + dy
                    pz = pos_z + dz
                    coordinates = (px, py, pz)

                    # Check if the new z is a valid altitude
                    if not self.perceived_world.is_valid_altitude(pz):
                        # ... and skip if it is not
                        continue

                    # Check if the new coordinates are out of bounds
                    if self.is_out_of_bounds(coordinates):
                        # ... and skip if this is the case
                        continue

                    # Check if the coordinates are already in the list of neighborhood
                    if coordinates not in neighborhood:
                        # Add Obstacle or "Empty"
                        if self.is_obstacle_at(coordinates):
                            self.perceived_world.place_obstacle_at(coordinates)
                        else:
                            self.perceived_world.place_empty_at(coordinates)
                        neighborhood.add(coordinates)

    def scan_for_uavs(self, pos):
        """
        Scan for UAVs in the neighborhood
        :param pos: Triple of coordinates
        :return: A list of UAVs that are close to the pos
        """
        neighborhood = set()
        other_uavs = set()

        pos_x, pos_y, pos_z = pos

        min_altitude_to_check = max(0, pos_z - self.sensor_range)
        max_altitude_to_check = min(self.sensor_range, self.perceived_world.get_max_altitude())

        # Add neighboring coordinates until the desired radius is reached
        for dy in range(-self.sensor_range, self.sensor_range + 1):
            for dx in range(-self.sensor_range, self.sensor_range + 1):
                for dz in range(min_altitude_to_check, max_altitude_to_check):
                    # Calculate new coordinates
                    px = pos_x + dx
                    py = pos_y + dy
                    pz = pos_z + dz
                    coordinates = (px, py, pz)

                    # Check if the new z is a valid altitude
                    if not self.perceived_world.is_valid_altitude(pz):
                        # ... and skip if it is not
                        continue

                    # Check if the new coordinates are out of bounds
                    if self.is_out_of_bounds(coordinates):
                        # ... and skip if this is the case
                        continue

                    # Check if the coordinates are already in the list of neighborhood
                    if coordinates not in neighborhood:
                        neighborhood.add(coordinates)

        for agent in self.agents:
            if agent.pos in neighborhood and agent not in other_uavs and agent.pos is not pos:
                other_uavs.add(agent)

        return other_uavs
