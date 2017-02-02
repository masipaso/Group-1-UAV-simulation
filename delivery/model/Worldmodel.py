import configparser
import random
import numpy as np
from PIL import Image
from mesa import Model
from mesa.datacollection import DataCollector

from delivery.grid.Static_grid import StaticGrid

from delivery.agents.BaseStation import BaseStation
from delivery.agents.Item import Item
from delivery.agents.uav.Uav import Uav
from delivery.schedule.Schedule import RandomActivationByType


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

        # Read landscape
        background_image = Image.open('./delivery/visualization/images/city500x500.jpg')
        background = background_image.load()

        # Configure schedule for Uavs and BaseStations
        self.schedule = RandomActivationByType(self)
        # Configure schedule for items
        self.item_schedule = RandomActivationByType(self)
        # Set parameters for ...
        # ... Grid
        self.width = config.getint('Grid', 'width')
        self.height = config.getint('Grid', 'height')
        self.pixel_ratio = config.getint('Grid', 'pixel_ratio')
        self.max_altitude = config.getint('Grid', 'max_altitude')
        self.min_altitude = 1
        # ... BaseStations
        self.range_of_base_station = config.getint('Basestation', 'range_of_base_station')
        self.number_of_uavs_per_base_station = config.getint('Uav', 'number_of_uavs_per_base_station')
        # ... UAV
        self.max_charge = config.getint('Uav', 'max_charge')
        self.battery_low = config.getint('Uav', 'battery_low')
        self.battery_decrease_per_step = config.getint('Uav', 'battery_decrease_per_step')
        self.battery_increase_per_step = config.getint('Uav', 'battery_increase_per_step')
        self.uav_default_altitude = config.getint('Uav', 'uav_default_altitude')
        self.sensor_range = config.getint('Uav', 'sensor_range')

        # Counter for number of steps
        self.steps = 0

        # Create the StaticGrid that contains the landscape (Obstacles, BaseStations, ...)
        self.landscape = StaticGrid(self.width, self.height, self.pixel_ratio, background)

        # Add data collector
        self.datacollector = DataCollector(
            {
                "UAVS": lambda m: m.schedule.get_type_count(Uav),
                "Items (Waiting)": self.compute_number_of_items,
                "Items (Picked up)": self.compute_number_of_picked_up_items,
                "Items (Delivered)": self.compute_number_of_delivered_items,
                "Average Walk Length": self.compute_average_walk_length,
                "Standard Deviation of Average Walk Lengths": self.compute_standard_deviation_walk_lengths,
                "Walklength Divided by Distance": self.compute_walk_length_divided_by_distance,
                "Average lifetime of item": self.compute_item_average_lifetime,
             }
        )

        # In the beginning there are no delivered Items
        # TODO: Make this beautiful
        self.number_of_delivered_items = 0

        # Populate the grid with obstacles and stuff
        self.populate_grid()

        self.running = True

    def step(self):
        """
        Advance the model one step
        """
        print("Step {}".format(self.steps))
        self.schedule.step()
        # Increase number of steps
        self.steps += 1
        self.item_schedule.step()
        # self.datacollector.collect(self)
        # dataframe = self.datacollector.get_model_vars_dataframe()
        # dataframe.to_csv('out.csv')

    def populate_grid(self):
        """
        Populate the grid with Obstacles, BaseStations and Uavs
        """

        # Populate the background with static Obstacles
        self.landscape.populate_grid()
        print("Obstacles done")

        # Create BaseStations
        base_stations = self.create_base_stations()
        print("BaseStations done")

        # Create UAVs
        uid = 0
        for base_station in base_stations:
            uid += 1
            for i in range(self.number_of_uavs_per_base_station):
                self.create_uav(uid + i, base_station)
        print("UAVs done")

    def create_base_stations(self):
        """
        Calculate how many base stations need to be created and create them
        :returns A list of BaseStations
        """
        base_stations = []
        width = 2 * self.range_of_base_station
        height = 2 * self.range_of_base_station
        number_of_base_stations = int((self.width * self.height) / (width * height))
        x = width
        y = height
        for i in range(0, number_of_base_stations):
            base_stations.append(self.create_base_station(i, (round(x - self.range_of_base_station), round(y - self.range_of_base_station))))
            if x + width > self.width:
                y += height
                x = width
            else:
                x += width
        return base_stations

    def create_base_station(self, bid, pos):
        """
        Create a BaseStation at a given position or close to it
        :param bid: unique identifier of the BaseStation
        :param pos: Tuple of coordinates
        :return The created BaseStation
        """
        x, y = pos
        # Store available cells
        available_cells = []
        radius = 1
        # If the center is an empty cell
        while not available_cells:
            # ... get neighboring cells and center cell
            neighborhood = self.landscape.get_neighborhood(pos, True, radius)

            # ... search the neighborhood and center
            for coordinates in neighborhood:
                # ... check if there is an obstacle
                for altitude in range(1, self.max_altitude + 1):
                    if self.landscape.is_obstacle_at(coordinates, altitude):
                        # ... and add the cell to the list of possible cells
                        available_cells.append(coordinates)

            # Increase the search radius if there are no possible cells
            radius += 1

        # If there are available cells, choose the cell that has at least one non-obstacle-neighbor
        # Store possible cells
        possible_cells = []
        for cell in available_cells:
            # ... get neighboring cells without center cell
            neighborhood = self.landscape.get_neighborhood(cell, False, 1)

            # ... search the neighborhood
            for coordinates in neighborhood:
                # ... check if there is an obstacle
                for altitude in range(1, self.max_altitude + 1):
                    if not self.landscape.is_obstacle_at(coordinates, altitude):
                        # ... and add the cell to the list of possible cells if there is one adjacent cell
                        # without an Obstacle
                        possible_cells.append(cell)
                        break

        # If there are possible cells, choose one at random
        pos_x, pos_y = random.choice(possible_cells)
        # Create the BaseStation
        base_station = BaseStation(model=self, pos=(pos_x, pos_y, self.min_altitude), bid=bid, center=(x, y),
                                   range_of_base_station=self.range_of_base_station)
        # Place the BaseStation on the landscape
        self.landscape.place_base_station((pos_x, pos_y))
        # Add the BaseStation to the schedule
        self.schedule.add(base_station)
        return base_station

    def create_uav(self, uid, base_station):
        """
        Create a Uav
        :param uid: unique identifier of the Uav
        :param base_station: the assigned BaseStation
        """
        pos_x, pos_y, pos_z = base_station.get_pos()
        # Create the uav
        position = (pos_x, pos_y, pos_z)
        uav = Uav(self, pos=position, uid=uid, max_charge=self.max_charge, battery_low=self.battery_low,
                  base_station=base_station, battery_decrease_per_step=self.battery_decrease_per_step,
                  battery_increase_per_step=self.battery_increase_per_step, altitude=self.uav_default_altitude,
                  max_altitude=self.max_altitude, sensor_range=self.sensor_range)
        # Add the Uav to the schedule
        self.schedule.add(uav)

    @staticmethod
    def compute_number_of_items(model):
        """
        Compute the number of items that are currently in a base station
        :return: number of items located in all base stations
        """
        number_of_items = 0
        for base_station in model.schedule.agents_by_type[BaseStation]:
            number_of_items += base_station.get_number_of_items()
        return number_of_items

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
            return sum(average_walks) / len(average_walks)
        else:
            return 0

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
    def compute_walk_length_divided_by_distance(model):
        length_by_distance = []

        for uav in model.schedule.agents_by_type[Uav]:
            for elem in uav.get_initial_delivery_distance_divided_by_average_walk_length():
                length_by_distance.append(elem)
        if len(length_by_distance) > 0:
            return sum(length_by_distance) / len(length_by_distance)
        else:
            return 0

    @staticmethod
    def compute_item_average_lifetime(model):
        result = 0
        if not model.item_schedule.agents_by_type[Item] == []:
            for item in model.item_schedule.agents:
                result = result + item.lifetime
            return result / len(model.item_schedule.agents)
        else:
            return 0
