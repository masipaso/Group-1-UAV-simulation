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
         # neighborhood = self.landscape.get_neighborhood((pos_x, pos_y), True, self.sensor_range)
        # for coordinates in neighborhood:
        #     for temp_altitude in range(pos_z - self.sensor_range, pos_z + self.sensor_range):
        #         if not self.perceived_world.is_valid_altitude(temp_altitude):
        #             continue
        #         if self.is_obstacle_at(coordinates + (temp_altitude,)):
        #             self.perceived_world.place_obstacle_at(coordinates + (temp_altitude,))
        #         else:
        #             self.perceived_world.place_empty_at(coordinates + (temp_altitude,))

        # pos_x, pos_y, pos_z = pos
        # not_looked_at = {pos}
        #
        # possible_neighbors = [(0, 1, 0), (1, 0, 0), (0, -1, 0), (-1, 0, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0),
        #                       (0, 1, 1), (1, 0, 1), (0, -1, 1), (-1, 0, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1),
        #                       (0, 1, -1), (1, 0, -1), (0, -1, -1), (-1, 0, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1), (-1, 1, -1),
        #                       (0, 0, 1), (0, 0, -1), (0, 0, 0)]
        #
        # for x, y, z in possible_neighbors:
        #     current_x = x + pos_x
        #     current_y = y + pos_y
        #     current_z = z + pos_z
        #
        #     not_looked_at.add((current_x, current_y, current_z))
        #
        #     if not self.perceived_world.is_valid_altitude(current_z):
        #         continue
        #
        #     if self.is_out_of_bounds((current_x, current_y, current_z)):
        #         continue
        #
        #     print(current_x, current_y, current_z)
        #
        #     if self.is_obstacle_at((current_x, current_y, current_z)):
        #         self.perceived_world.place_obstacle_at((current_x, current_y, current_z))
        #     else:
        #         self.perceived_world.place_empty_at((current_x, current_y, current_z))

        neighborhood = set()

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
        pos_x, pos_y, pos_z = pos
        other_uavs = []
        neighborhood = self.grid.get_neighborhood(pos=(pos_x, pos_y), moore=True, include_center=False, radius=self.sensor_range)
        for cell in neighborhood:
            for obj in self.grid.get_cell_list_contents(cell):
                # Check if the obj is NOT a BaseStation
                if type(obj) is not BaseStation:
                    other_uavs.append(obj)
        return other_uavs
