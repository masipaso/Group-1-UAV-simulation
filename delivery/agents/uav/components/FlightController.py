from delivery.agents.BaseStation import BaseStation
# Import utils
from delivery.utils.get_euclidean_distance import get_euclidean_distance
from operator import itemgetter
from heapq import *

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
        print("Scanning start {}".format(datetime.now().time()))
        self.uav.sensor.scan(self.uav.pos)
        print("Scanning end {}".format(datetime.now().time()))

        # Store the shortest path
        shortest_path = []
        # Store cells that were excluded from the search for a best_cell because they are not accessible from the
        # current position of the UAV
        excluded_cells = []
        # Store the best possible cell that the UAV should move towards
        best_cell = None

        # As long as there is no shortest path to the best_cell ...
        while not shortest_path:
            # ... get the best possible cell that is currently in sensor_range
            print("Finding best cell {}".format(datetime.now().time()))
            best_cell = self._get_best_cell(excluded_cells)
            print("Found best cell {}".format(datetime.now().time()))
            print("best cell {}".format(best_cell))

            if best_cell is None:
                # If all cells are excluded from the search, then the UAV can't move
                print(' Agent: {} cannot move.'.format(self.uav.uid))
                return None

            # ... and calculate the shortest path to it
            print("Finding shortest path to best cell {}".format(datetime.now().time()))
            shortest_path = self._get_shortest_path_between(self.uav.pos, best_cell)
            print("Found shortest path to best cell {}".format(datetime.now().time()))
            print(shortest_path)

        # Get the next cell on the shortest path
        next_cell = shortest_path.pop()
        print("{} moves from {} to {} on its way to {}".format(self.uav.uid, self.uav.pos, next_cell, best_cell))
        self.move_to(next_cell)

    def _get_best_cell(self, excluded_cell):
        """
        Get the best possible cell that is known to the UAV. Best possible means that being on that cell minimizes
        the remaining distance to the destination.
        :param excluded_cell: A list of cells that are excluded as best cell
        :return: A triple of coordinates representing the best possible cell
        """
        min_distance = None
        best_cell = None

        # Iterate over all altitudes ...
        for altitude in range(1, self.uav.max_altitude + 1):
            # Check if the altitude is a valid
            if not self.uav.perceived_world.is_valid_altitude(altitude):
                # ... and skip if it is not
                continue
            for coordinates in self.uav.perceived_world.get_known_coordinates_at(altitude):
                coordinates = coordinates + (altitude,)
                # If the coordinates and altitude are excluded ...
                if coordinates in excluded_cell:
                    continue
                # If there is no Obstacle at the altitude ...
                if not self.uav.perceived_world.is_obstacle_at(coordinates):
                    # ... then there might be a BaseStation or nothing ...
                    # ... calculate the remaining distance from the coordinates to the destination of the UAV
                    distance = get_euclidean_distance(self.uav.destination, coordinates)
                    if min_distance is None:
                        min_distance = distance
                    else:
                        if min_distance > distance:
                            min_distance = distance
                            best_cell = coordinates
        return best_cell

    def _get_shortest_path_between(self, start, goal):
        """
        Get the shortest path between two tuples of coordinates
        :param start: Triple of coordinates of the current position
        :param goal: Triple of coordinates of the desired target position
        :return: List of steps of the shortest path
        """

        # A list representing the allowed movements of the UAV. N, E, S, W, NE, SE, SW, NW, ascend straight up, descent
        # straight down
        allowed_movements = [(0, 1, 0), (1, 0, 0), (0, -1, 0), (-1, 0, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0),
                             (-1, 1, 0), (0, 0, 1), (0, 0, -1)]
        # A set of already "visited cells"
        visited_cells = set()
        # A dictionary to track the path
        came_from = {}
        # A dictionary to track the "costs" of getting to a certain cell
        g_score = {start: 0}
        # A dictionary to track the total "costs" of getting from the start to the goal and visiting a certain cell
        f_score = {start: get_euclidean_distance(start, goal)}
        # A list of cells that are not "visited" yet
        unvisited_cells = []
        # To sort the unvisited cells by there f_score
        heappush(unvisited_cells, (f_score[start], start))

        # As long as there are unvisited cells ...
        while unvisited_cells:
            # ... take the cell with the lowest f_score ...
            current = heappop(unvisited_cells)[1]
            # ... check if it is the goal
            if current == goal:
                # If that is the case return the found path
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data

            # ... "mark" it as visited
            visited_cells.add(current)
            # ... and check all neighboring cells (according to the allowed_movements)
            for x, y, z in allowed_movements:
                # Get the coordinates of the neighboring cell
                neighbor_cell = current[0] + x, current[1] + y, current[2] + z
                # Check if it has a valid altitude ...
                if self.uav.perceived_world.is_valid_altitude(neighbor_cell[2]):
                    # ... if it is known to the UAV ...
                    if self.uav.perceived_world.is_known(neighbor_cell):
                        # ... and if there is no Obstacle
                        if not self.uav.perceived_world.is_obstacle_at(neighbor_cell):
                            # Calculate the new g_score for the neighboring cell
                            temp_g_score = g_score[current] + get_euclidean_distance(current, neighbor_cell)
                            # If the neighboring cell was already visited and the new g_score is bigger than the g_score
                            # that is already known ...
                            if neighbor_cell in visited_cells and temp_g_score >= g_score.get(neighbor_cell, 0):
                                continue
                            # If the new g_score is smaller than the already known g_score or the neighboring cell is
                            # not listed as unvisited ...
                            if temp_g_score < g_score.get(neighbor_cell, 0) or neighbor_cell not in [i[1] for i in
                                                                                                     unvisited_cells]:
                                # Save the path
                                came_from[neighbor_cell] = current
                                # Save the g_score
                                g_score[neighbor_cell] = temp_g_score
                                # Calculate the total "costs"
                                f_score[neighbor_cell] = temp_g_score + get_euclidean_distance(neighbor_cell, goal)
                                # Add the neighboring cell to the unvisited cells
                                heappush(unvisited_cells, (f_score[neighbor_cell], neighbor_cell))
        return []

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

    def move_to(self, pos):
        """
        Move an UAV to a position
        :param pos: Triple of coordinates where the UAV should move to
        """
        pos_x, pos_y, pos_z = pos
        self.uav.model.grid._remove_agent((pos_x, pos_y), self.uav)
        self.uav.model.grid._place_agent(self.uav, (pos_x, pos_y))
        # self.uav.model.grid.move_agent(self.uav, (pos_x, pos_y))
        # Reset the position of the UAV because the MultiGrid sets it to a 2D position
        self.uav.pos = pos