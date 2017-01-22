from delivery.agents.Repellent import Repellent
from delivery.agents.BaseStation import BaseStation
# Import utils
from delivery.utils.Step import Step
from delivery.utils.Cell import Cell
from delivery.utils.get_step_distance import get_step_distance
from delivery.utils.get_euclidean_distance import get_euclidean_distance
from operator import itemgetter

from datetime import datetime


class FlightController:
    """
    The FlightController decides where to fly next
    """
    # TODO: More details

    def __init__(self, uav):
        """
        Initialize the FlightController
        :param uav: The UAV to which the FlightController belongs
        """
        self.uav = uav

    def make_step(self):
        """
        Advance the UAV by one step
        """
        # If the Uav does not have a destination, do nothing
        if self.uav.destination is None:
            print(' Agent: {} has no destination.'.format(self.uav.uid))
            return None

        # Initiate scan of the neighborhood
        self.uav.sensor.scan(self.uav.pos, self.uav.altitude)

        # Get the best possible cell that is currently in sensor_range
        best_cell = self._get_best_cell()

        # Calculate the shortest path to the best possible cell
        shortest_path = self._get_shortest_path_between(self.uav.pos, best_cell.pos, best_cell.altitude)
        # Get the next cell on the shortest path
        next_cell = shortest_path.pop(0)
        print("Next step for {} is: {} {}".format(self.uav.uid, next_cell.pos, next_cell.altitude))
        self.move_to(next_cell.pos, next_cell.altitude)

    def _get_best_cell(self):
        """
        Get the best possible cell that is known to the UAV
        :return: A Step, which is the best possible one according to the distance to the destination
        """
        possible_steps = []

        # Iterate over all altitudes ...
        for altitude in range(0, self.uav.max_altitude):
            for coordinates in self.uav.perceived_world.get_known_coordinates_at(altitude):
                # If there is no Obstacle at the altitude ...
                if not self.uav.perceived_world.is_obstacle_at(coordinates, self.uav.altitude):
                    # ... then there might be a BaseStation (-1) or nothing (0)
                    # Calculate the distance from the coordinates to teh destination of the UAV
                    distance = get_euclidean_distance(self.uav.destination, coordinates)
                    possible_steps.append(self._create_step(distance, coordinates, altitude))

        # Sort all possible Steps by distance
        possible_steps.sort(key=lambda step: step.distance)
        # Get the best possible Step
        return possible_steps[0]

    def _get_shortest_path_between(self, pos, target, altitude):
        """
        Get the shortest path between two tuples of coordinates
        :param pos: Tuple of coordinates of the current position (start)
        :param target: Tuple of coordinates of the desired target position
        :param altitude:
        :return:
        """
        visited_cells = self._search_paths(pos, target, altitude)
        # Get the target cell
        cell = next((cell for cell in visited_cells if cell.pos == target and cell.altitude is altitude), None)
        path = [cell]
        while cell.parent:
            cell = cell.parent
            path.append(cell)
        path.reverse()
        return path

    def _search_paths(self, pos, target, altitude):
        """
        Search for paths between pos and target
        :param pos: Tuple of coordinates of the current position (start)
        :param target: Tuple of coordinates of the desired target position
        :param altitude:
        :return: A set of all visited cells
        """
        print(datetime.now().time())
        # Store the visited cells
        visited_cells = set()

        # Get the neighboring cells of the UAV
        unvisited_cells = self._get_cells_around(pos)

        # Perform A*
        while len(unvisited_cells):
            unvisited_cells.sort(key=lambda cell: cell.f)
            # Pop a Cell from the heap queue
            current_cell = unvisited_cells.pop(0)
            # Add the Cell to the visited_cells
            visited_cells.add(current_cell)
            # If this is the target ...
            if current_cell.pos == target and current_cell.altitude is altitude:
                print(datetime.now().time())
                return visited_cells
            # Get neighboring cells for Cell
            neighborhood = self._get_cells_around(current_cell.pos)
            for neighboring_cell in neighborhood:
                # If the cell was not already visited ...
                if not any(cell.pos == neighboring_cell.pos and cell.altitude == neighboring_cell.altitude for cell in visited_cells):
                    duplicate = False
                    # Check if the Cell is in the unvisited_cells ...
                    for cell in unvisited_cells:
                        if cell.pos == neighboring_cell.pos and cell.altitude == neighboring_cell.altitude:
                            neighboring_cell = cell
                            duplicate = True
                    # Update the cell or add it to the unvisited_cells
                    if duplicate:
                        # ... adjust the path, if the new one is better
                        if neighboring_cell.g > current_cell.g + 1:
                            # Update the cell
                            neighboring_cell.update(current_cell.g + 1, get_euclidean_distance(current_cell.pos, neighboring_cell.pos), current_cell)
                    else:
                        neighboring_cell.update(current_cell.g + 1, get_euclidean_distance(current_cell.pos, neighboring_cell.pos), current_cell)
                        unvisited_cells.append(neighboring_cell)

    def _get_cells_around(self, pos):
        """
        Get all cells that surround a position
        :param pos: Tuple of coordinates
        :return: A List of Cells
        """
        x, y = pos
        x_cells = [x, x + 1, x - 1]
        y_cells = [y, y + 1, y - 1]
        cells = []

        for x_cell in x_cells:
            for y_cell in y_cells:
                pos = (x_cell, y_cell)
                # Don't add the cell the UAV is currently at
                if not (x is x_cell and y is y_cell):
                    if self.uav.perceived_world.is_known(pos, self.uav.altitude) and not self.uav.perceived_world.is_obstacle_at(pos, self.uav.altitude):
                        cells.append(Cell(pos, self.uav.altitude))
                if self.uav.altitude + 1 <= self.uav.max_altitude and self.uav.perceived_world.is_known(pos, self.uav.altitude + 1) and not self.uav.perceived_world.is_obstacle_at(pos, self.uav.altitude + 1):
                    cells.append(Cell(pos, self.uav.altitude + 1))
                if self.uav.altitude - 1 >= 0 and self.uav.perceived_world.is_known(pos, self.uav.altitude - 1) and not self.uav.perceived_world.is_obstacle_at(pos, self.uav.altitude - 1):
                    cells.append(Cell(pos, self.uav.altitude - 1))
        return cells

    def get_nearest_base_station(self):
        """
        Get the BaseStation that is closest to the UAV
        :return: The nearest BaseStation
        """
        # Based on euclidean distance, select closest baseStation
        base_stations = self.uav.model.schedule.agents_by_type[BaseStation]
        base_stations_by_distance = []
        for station in base_stations:
            base_stations_by_distance.append((station.pos, get_euclidean_distance(self.uav.pos, station.pos)))
            base_stations_by_distance.sort(key=lambda tup: tup[1])
        return base_stations_by_distance.pop(0)[0]

    def choose_base_station_to_pick_up_item_from(self):
        """
        Choose a BaseStation to pick up an Item
        :return: The nearest BaseStations
        """
        # Based on number of items and distance of BaseStation, select next BaseStation to pick up items from
        # TODO: This should be decentralized in the next step!
        base_stations = self.uav.model.schedule.agents_by_type[BaseStation]
        base_stations_by_distance = []
        for station in base_stations:
            base_stations_by_distance.append((station.pos, get_euclidean_distance(self.uav.pos, station.pos),
                                              len(station.items)))
            sorted(base_stations_by_distance,  key=itemgetter(2,1))
        print("List of BaseStations: {}".format(base_stations_by_distance))
        return base_stations_by_distance.pop(0)[0]

    def move_to(self, pos, altitude):
        """
        Move an UAV to a position
        :param pos: Tuple of coordinates where the UAV should move to
        :param altitude: Altitude to which the UAV should ascend/descend to
        """
        self.uav.model.grid.move_agent(self.uav, pos)
        self.uav.altitude = altitude

    def _create_step(self, distance, pos, altitude):
        """
        Create a new Step
        :param distance:
        :param pos:
        :param altitude:
        :return:
        """
        return Step(distance=distance, pos=pos, altitude=altitude)