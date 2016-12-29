import configparser
import random
import math
import numpy as np
from random import randint
from PIL import Image
from mesa import Model
from mesa.datacollection import DataCollector

from delivery.agents.baseStation import BaseStation
from delivery.agents.obstacle import Obstacle
from delivery.agents.uav import Uav
from delivery.grid.multi_grids import TwoMultiGrid
from delivery.schedule.schedule import RandomActivationByType


class WorldModel(Model):
    """
    Model for representing the world
    """

    def __init__(self):
        """
        Create a new WorldModel with the given parameters
        """
        super().__init__()
        # Read config.cfg
        config = configparser.ConfigParser()
        config.read('./config.ini')

        # Read  and parse landscape
        landscape = Image.open('./delivery/visualization/images/test800x800.jpg')
        self.landscape = landscape.load()

        # Configure schedule for Uavs and BaseStations
        self.schedule = RandomActivationByType(self)
        # Configure schedule for Repellents
        self.repellent_schedule = RandomActivationByType(self)
        # Set parameters
        self.width = config.getint('Grid', 'width')
        self.height = config.getint('Grid', 'height')
        self.pixel_ratio = config.getint('Grid', 'pixel_ratio')
        self.range_of_base_station = config.getfloat('Basestation', 'range_of_base_station')
        self.number_of_uavs_per_base_station = config.getint('Uav', 'number_of_uavs_per_base_station')
        self.max_battery = config.getint('Uav','max_battery')
        self.battery_low = config.getint('Uav','battery_low')
        self.number_of_repellents= 0

        # Add a grid that is used to visualize the 'actual' world
        self.grid = TwoMultiGrid(self.height, self.width, torus=False)
        # Add a grid that is used to visualize the perceived world
        self.perceived_world_grid = TwoMultiGrid(self.height, self.width, torus=False)

        # Add data collector
        self.datacollector = DataCollector(
            {
                "UAVS": lambda m: m.schedule.get_type_count(Uav),
                "Items (Waiting)": self.compute_number_of_items,
                "Items (Picked up)": self.compute_number_of_picked_up_items,
                "Items (Delivered)": self.compute_number_of_delivered_items,
                "Average Walk Length": self.compute_average_walk_length,
                "Standard Deviation of Average Walk Lengths": self.compute_standard_deviation_walk_lengths,
                "Walklength Divided by Distance": self.compute_walklength_divided_by_distance,
             }
        )

        # In the beginning there are no delivered Items
        # TODO: Make this beautiful
        self.number_of_delivered_items = 0

        # Store all obstacles
        self.obstacles = np.zeros(shape=[self.width, self.height])

        # Populate the grid with obstacles and stuff
        self.populate_grid()

        self.running = True

    def step(self):
        """
        Advance the model one step
        """
        self.schedule.step()
        self.repellent_schedule.step()
        self.datacollector.collect(self)
        dataframe = self.datacollector.get_model_vars_dataframe()
        dataframe.to_csv('out.csv')

    def populate_grid(self):
        """
        Populate the grid with Obstacles, BaseStations and Uavs
        """

        multiplier = max(round(self.pixel_ratio / 2), 1)
        print(self.width, self.height, self.pixel_ratio, multiplier)

        # Read landscape to get locations of obstacles
        for j in range(1, self.height, multiplier):
            for i in range(1, self.width, multiplier):
                r, g, b = self.landscape[i, j]
                if self.is_obstacle_color(r, g, b):
                    fill_cells_x = []
                    fill_cells_y = []
                    for k in range(0, multiplier):
                        fill_cells_x.append(i - k)
                        fill_cells_y.append(self.height - j - k)

                    for x in fill_cells_x:
                        if 0 < x < self.width:
                            for y in fill_cells_y:
                                if 0 < y < self.height:
                                    self.create_obstacle(x, y)
                                else:
                                    break

        # Create Obstacles
        # for j in range(1, self.height, 5):
        #     for i in range(1, self.width, 5):
        #         form = randint(1, 2)
        #         if form == 1:
        #             self.make_l(i, j)
        #         if form == 2:
        #             self.make_u(i, j)
        #         if form == 3:
        #             self.make_square(i, j)

        print("Obstacles done")

        # Create BaseStations
        self.create_base_stations()
        print("BaseStations done")

        # Create Uavs
        id = 0
        for base_station in self.schedule.agents_by_type[BaseStation]:
            id += 1
            for i in range(self.number_of_uavs_per_base_station):
                self.create_uav(id + i, base_station)

        print("UAVs done")

    @staticmethod
    def is_obstacle_color(r, g, b):
        black = range(0, 10)
        return r in black and g in black and b in black

    def create_base_stations(self):
        """
        Calculate how many base stations need to be created and create them
        """
        width = 2 * self.range_of_base_station
        height = 2 * self.range_of_base_station
        number_of_base_stations = int((self.width * self.height) / (width * height))
        x = width
        y = height
        for i in range(0, number_of_base_stations):
            self.create_base_station(i, round(x - self.range_of_base_station), round(y - self.range_of_base_station))
            if x + width > self.width:
                y += height
                x = width
            else:
                x += width

    def create_uav(self, uid, base_station):
        """
        Create a Uav
        :param uid: unique identifier of the Uav
        :param base_station: the assigned BaseStation
        """
        # Create the uav
        uav = Uav(self, pos=base_station.get_pos(), id=uid, max_battery=self.max_battery, battery_low=self.battery_low, base_station=base_station)
        # Place the uav on the grids
        self.grid.place_agent(uav, base_station.get_pos())
        self.perceived_world_grid.place_agent(uav, base_station.get_pos())
        # Add the Uav to the schedule
        self.schedule.add(uav)

    def create_base_station(self, bid, x, y):
        """
        Create a BaseStation at a random location
        :param bid: unique identifier of the BaseStation
        :param x:
        :param y:
        """
        # Store available cells
        available_cells = []
        radius = 1
        # If the center is an empty cell
        while not available_cells:
            # ... get neighboring cells and center cell
            check_cells_x = [x, x + radius, x - radius]
            check_cells_y = [y, y + radius, y - radius]

            # ... search the neighborhood and center
            for x in check_cells_x:
                if 0 < x < self.width:
                    for y in check_cells_y:
                        if 0 < y < self.height:
                            # ... check if there is an obstacle
                            if math.isclose(self.obstacles[x, y], 1, rel_tol=1e-5):
                                # ... and add the cell to the list of possible cells
                                available_cells.append((x, y))
                        else:
                            break
                else:
                    break

            # Increase the search radius if there are no possible cells
            radius += 1

        # If there are available cells, choose the cell that has at least one non-obstacle-neighbor
        # Store possible cells
        possible_cells = []
        for cell in available_cells:
            # ... get neighboring cells
            check_cells_x = [x, x + radius, x - radius]
            check_cells_y = [y, y + radius, y - radius]

            for x in check_cells_x:
                if 0 < x < self.width:
                    for y in check_cells_y:
                        if 0 < y < self.height:
                            # Don't check the actual cell because we already know that it has an obstacle
                            if x is not cell[0] and y is not cell[1]:
                                # ... check if there is an obstacle
                                if not math.isclose(self.obstacles[x, y], 1, rel_tol=1e-5):
                                    # ... and add the cell to the list of possible cells
                                    possible_cells.append((cell[0], cell[1]))

        # If there are possible cells, choose one at random
        pos = random.choice(possible_cells)
        # Create the BaseStation
        base_station = BaseStation(model=self, pos=pos, id=bid, center=(x, y), range_of_base_station=self.range_of_base_station)
        # Place the BaseStation on the grids
        self.grid.place_agent(base_station, pos)
        self.perceived_world_grid.place_agent(base_station, pos)
        # Add the BaseStation to the schedule
        self.schedule.add(base_station)

        # Add the BaseStation to the obstacle list
        self.create_obstacle(pos[0], pos[1], 2)

    def create_obstacle(self, x, y, value=1):
        """
        Create one obstacle at the given position; the Obstacle can be either an Obstacle (value=1)
        or a BaseStation(value=2)
        :param x: x coordinate
        :param y: y coordinate
        :param value: the value that is stored at the given position
        :return:
        """
        self.obstacles[x][y] = value
        # obstacle = Obstacle(self, (x, y))
        # self.grid.place_agent(obstacle, (x, y))

    def make_l(self, i, j):
        """
        Create a l-shaped obstacle at a defined position
        :param i:
        :param j:
        """
        self.create_obstacle(i, j)

        for x in range(1, 4, 1):
            self.create_obstacle(i, j + x)

        for y in range(1, 4, 1):
            self.create_obstacle(i + y, j)

    def make_u(self, i, j):
        """
        Create a u-shaped obstacle at a defined position
        :param i:
        :param j:
        """
        self.create_obstacle(i, j)

        for x in range(1, 4, 1):
            self.create_obstacle(i, j + x)
            self.create_obstacle(i + 3, j + x)

        for y in range(1, 4, 1):
            self.create_obstacle(i + y, j)

    def make_square(self, i, j):
        """
        Create a square-shaped obstacle at a defined position
        :param i:
        :param j:
        """
        for x in range(1, 4, 1):
            self.create_obstacle(i, j + x)
            self.create_obstacle(i+3, j + x)

        for y in range(0, 4, 1):
            self.create_obstacle(i + y, j)

        self.create_obstacle(i + 1, j + 3)
        self.create_obstacle(i + 2, j + 3)

    @staticmethod
    def compute_number_of_items(model):
        """
        Compute the number of items that are currently in a base station
        :return: number of items located in all base stations
        """
        number_of_items = 0
        for base_station in model.schedule.agents_by_type[BaseStation]:
            number_of_items += base_station.get_number_of_items()
        return  number_of_items

    @staticmethod
    def compute_number_of_picked_up_items(model):
        """
        Compute the number of items that are currently delivered
        :return: number of items that are currently delivered
        """
        number_of_picked_up_items = 0
        for base_station in model.schedule.agents_by_type[BaseStation]:
            number_of_picked_up_items += base_station.get_number_of_items(picked_up=True)
        return number_of_picked_up_items

    @staticmethod
    def compute_number_of_delivered_items(model):
        """
        Computer the number of items that are already delivered
        :return: number of items that are already delivered
        """
        return model.number_of_delivered_items

    @staticmethod
    def compute_average_walk_length(model):
        average_walks = []

        for uav in model.schedule.agents_by_type[Uav]:
            for elem in uav.get_walk_lengths():
                average_walks.append(elem)
        if len(average_walks)>0:
            return sum(average_walks)/len(average_walks)
        else: return 0

    @staticmethod
    def compute_standard_deviation_walk_lengths(model):
        average_walks = []

        for uav in model.schedule.agents_by_type[Uav]:
            for elem in uav.get_walk_lengths():
                average_walks.append(elem)
        if len(average_walks) > 0:
            return np.std(average_walks)
        else:
            return 0

    @staticmethod
    def compute_walklength_divided_by_distance(model):
        length_by_distance = []

        for uav in model.schedule.agents_by_type[Uav]:
            for elem in uav.get_initial_delivery_distance_divided_by_average_walk_length():
                length_by_distance.append(elem)
        if len(length_by_distance) > 0:
            return sum(length_by_distance)/len(length_by_distance)
        else:
            return 0