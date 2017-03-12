import sys
import configparser
import random
import math
import numpy as np
from PIL import Image
from mesa import Model
from mesa.datacollection import DataCollector

from delivery.grid.StaticGrid import StaticGrid

from delivery.agents.BaseStation import BaseStation
from delivery.agents.Item import Item
from delivery.agents.uav.Uav import Uav
from delivery.schedule.Schedule import Schedule


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

        self.background_image_source = config.get('Grid', 'image', fallback='./delivery/visualization/images/a_city500x500.jpg')
        if type(self.background_image_source) is not str:
            print("[Configuration] The image is not valid.")
            sys.exit(1)

        try:
            test_background_image_source = self.background_image_source.split("/").pop()
            test_background_image_source = test_background_image_source.split(".")
            if test_background_image_source[len(test_background_image_source) - 1] != "jpg":
                raise ValueError
        except Exception:
            print("[Configuration] The image is not valid.")
            sys.exit(1)

        # Read landscape
        try:
            background_image = Image.open(self.background_image_source)
            background = background_image.load()
        except FileNotFoundError:
            print("[Configuration] The image could not be found.")
            sys.exit(1)

        # Configure schedule for UAVs and BaseStations
        self.schedule = Schedule(self)
        # Configure schedule for items
        self.item_schedule = Schedule(self)
        # Set parameters for ...
        # ... Grid
        self.width, self.height = background_image.size
        try:
            self.pixel_ratio = config.getint('Grid', 'pixel_ratio', fallback=10)
        except ValueError:
            print("[Configuration] The pixel_ratio is not valid.")
            sys.exit(1)

        try:
            self.max_altitude = config.getint('Grid', 'max_altitude', fallback=4)
        except ValueError:
            print("[Configuration] The max_altitude is not valid.")
            sys.exit(1)
        # ... BaseStations
        try:
            self.range_of_base_station = config.getint('Base_station', 'range_of_base_station', fallback=125)
        except ValueError:
            print("[Configuration] The range_of_base_station is not valid.")
            sys.exit(1)

        try:
            self.number_of_uavs_per_base_station = config.getint('UAV', 'number_of_uavs_per_base_station', fallback=2)
        except ValueError:
            print("[Configuration] The number_of_uavs_per_base_station is not valid.")
            sys.exit(1)
        # ... UAV
        try:
            self.max_charge = config.getint('UAV', 'max_charge', fallback=1000)
        except ValueError:
            print("[Configuration] The max_charge is not valid.")
            sys.exit(1)

        try:
            self.battery_low = config.getint('UAV', 'battery_low', fallback=500)
        except ValueError:
            print("[Configuration] The battery_low is not valid.")
            sys.exit(1)

        try:
            self.battery_decrease_per_step = config.getint('UAV', 'battery_decrease_per_step', fallback=1)
        except ValueError:
            print("[Configuration] The battery_decrease_per_step is not valid.")
            sys.exit(1)

        try:
            self.battery_increase_per_step = config.getint('UAV', 'battery_increase_per_step', fallback=10)
        except ValueError:
            print("[Configuration] The battery_increase_per_step is not valid.")
            sys.exit(1)

        try:
            self.sensor_range = config.getint('UAV', 'sensor_range', fallback=5)
        except ValueError:
            print("[Configuration] The sensor_range is not valid.")
            sys.exit(1)

        # Counter for number of steps
        self.steps = 0

        # Store the agent that should be send to the client for more details
        self.details_for = None

        # Create the StaticGrid that contains the landscape (obstacles, base stations, ...)
        self.landscape = StaticGrid(self.width, self.height, background)

        # Add data collector
        self.datacollector = DataCollector(
            {
                "UAVS": lambda m: m.schedule.get_type_count(Uav),
                "Items (Waiting)": self.compute_number_of_items,
                "Items (Picked up)": self.compute_number_of_picked_up_items,
                "Items (Delivered)": self.compute_number_of_delivered_items,
                "Average Delivery Walk Length": self.compute_average_walk_length,
                "Standard Deviation of Average Walk Lengths": self.compute_standard_deviation_walk_lengths,
                "Walklength Divided by Distance": self.compute_walk_length_divided_by_distance,
                "Average lifetime of item": self.compute_item_average_lifetime,
             }
        )

        # In the beginning there are no delivered Items
        self.number_of_delivered_items = 0

        try:
            # Populate the grid with obstacles and BaseStations and UAVs
            self.populate_grid()
        except RuntimeError as error:
            print(error)
            sys.exit(1)

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
        self.datacollector.collect(self)
        dataframe = self.datacollector.get_model_vars_dataframe()
        dataframe.to_csv('out.csv')

    def populate_grid(self):
        """
        Populate the grid with obstacles, BaseStations and UAVs
        """

        # Populate the background with static obstacles
        self.landscape.populate_grid()

        image = Image.new("RGBA", (self.width, self.height))
        for x in range(0, self.width):
            for y in range(0, self.height):
                image.putpixel((x, self.height - y - 1), self.landscape.get_obstacle_color((x, y)))
            image.putpixel((x, self.height - 1), self.landscape.get_obstacle_color((x, 1)))

        file_name = self.background_image_source.split("/").pop()
        new_file_name = file_name.split(".")
        new_file_name.pop()
        new_file_name = new_file_name.pop()
        new_file_name += "_obstacles.png"
        image.save("./delivery/visualization/images/" + new_file_name)
        print("Obstacles done")

        # Create base stations
        base_stations = self.create_base_stations()
        print("BaseStations done")

        # Create UAVs
        uid = 0
        for base_station in base_stations:
            for i in range(self.number_of_uavs_per_base_station):
                uid += 1
                self.create_uav(uid, base_station)
        print("UAVs done")

    def create_base_stations(self):
        """
        Calculate how many BaseStations need to be created and create them
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
        available_cells = set()
        # To check if the coordinates are already stored
        available_cells_helper = set()
        radius = 1
        # If the center is an empty cell
        while not available_cells:
            # ... get neighboring cells and center cell
            neighborhood = self.landscape.get_neighborhood(pos, True, radius)

            # ... search the neighborhood and center
            for coordinates in neighborhood:
                # ... check if there is an obstacle
                for altitude in range(self.max_altitude, 0, -1):
                    if self.landscape.is_obstacle_at_exact(coordinates, altitude):
                        if coordinates not in available_cells_helper:
                            # ... and add the cell to the list of available cells if at least one neighboring cell is not
                            # filled with an obstacle
                            temp_neighborhood = self.landscape.get_neighborhood(coordinates, False, 1)
                            for temp_coordinates in temp_neighborhood:
                                if not self.landscape.is_obstacle_at_exact(temp_coordinates, altitude):
                                    available_cells.add(coordinates + (altitude,))
                                    available_cells_helper.add(coordinates)

            # Increase the search radius if there are no possible cells
            radius += 1

            if radius > self.range_of_base_station:
                raise RuntimeError(
                    'There is no obstacle that fulfills the requirement to be a valid location for a base '
                    'station. A base station needs to be place on top of an obstacle and has to have at least '
                    'one neighboring cell that is not occupied by an obstacle.')

        # If there are available cells, choose one at random
        pos_x, pos_y, pos_z = random.sample(available_cells, 1)[0]

        # Create the BaseStation
        base_station = BaseStation(model=self, pos=(pos_x, pos_y, pos_z), bid=bid, center=(x, y),
                                   range_of_base_station=self.range_of_base_station)
        # Place the BaseStation on the landscape
        self.landscape.place_base_station((pos_x, pos_y))
        # Add the BaseStation to the schedule
        self.schedule.add(base_station)
        return base_station

    def create_uav(self, uid, base_station):
        """
        Create a UAV
        :param uid: unique identifier of the Uav
        :param base_station: the assigned BaseStation
        """
        pos_x, pos_y, pos_z = base_station.get_pos()
        # Create the UAV
        position = (pos_x, pos_y, pos_z)
        uav = Uav(self, pos=position, uid=uid, max_charge=self.max_charge, battery_low=self.battery_low,
                  base_station=base_station, battery_decrease_per_step=self.battery_decrease_per_step,
                  battery_increase_per_step=self.battery_increase_per_step, max_altitude=self.max_altitude,
                  sensor_range=self.sensor_range)
        # Add the UAV to the schedule
        self.schedule.add(uav)

    def get_details_for(self, pos):
        """
        Pick an agent based on the position
        :param pos: Tuple of coordinates (not normalized)
        :return: An agent, if there is an agent at the requested position. Otherwise, None
        """
        pos_x, pos_y = pos
        pos_x = math.floor(pos_x / self.pixel_ratio)
        pos_y = math.floor(pos_y / self.pixel_ratio)
        # Search for BaseStations
        for baseStation in self.schedule.agents_by_type[BaseStation]:
            if pos_x == baseStation.pos[0] and pos_y == baseStation.pos[1]:
                return baseStation
        # Search for UAVs
        for UAV in self.schedule.agents_by_type[Uav]:
            if pos_x == UAV.pos[0] and pos_y == UAV.pos[1]:
                return UAV
        # Search for Items
        for item in self.item_schedule.agents_by_type[Item]:
            if pos_x == item.pos[0] and pos_y == item.pos[1]:
                return item

        return None

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
        :param model: The model that the calculation is for
        :return: Number of items that are already delivered
        """
        return model.number_of_delivered_items

    @staticmethod
    def compute_average_walk_length(model):
        """
        Compute the average walk length for all UAVs
        :param model: The model that the calculation is for
        :return: The average walk length
        """
        average_walks = []

        for uav in model.schedule.agents_by_type[Uav]:
            for elem in uav.get_walk_lengths():
                average_walks.append(elem)
        if len(average_walks) > 0:
            return sum(average_walks) / len(average_walks)
        else:
            return 0

    @staticmethod
    def compute_standard_deviation_walk_lengths(model):
        """
        Compute the standard deviation in walk lengths of all UAVs
        :param model: The model that the calculation is for
        :return: The standard deviation of all walk length
        """
        walks = []

        for uav in model.schedule.agents_by_type[Uav]:
            for elem in uav.get_walk_lengths():
                walks.append(elem)
        if len(walks) > 0:
            return np.std(walks)
        else:
            return 0

    @staticmethod
    def compute_walk_length_divided_by_distance(model):
        """
        Compute the ratio between the actual walk and the initial calculated distance
        :param model: The model that the calculation is for
        :return: The ratio between the actual walk and the initial distance
        """
        initial_length_by_distance = []

        for uav in model.schedule.agents_by_type[Uav]:
            for elem in uav.get_walk_length_divided_by_initial_distance():
                initial_length_by_distance.append(elem)
        if len(initial_length_by_distance) > 0:
            return sum(initial_length_by_distance) / len(initial_length_by_distance)
        else:
            return 0

    @staticmethod
    def compute_item_average_lifetime(model):
        """
        Compute the average lifetime of an Item
        :param model: The model that the calculation is for
        :return: The average lifetime of an Item
        """
        result = 0
        if not model.item_schedule.agents_by_type[Item] == []:
            for item in model.item_schedule.agents:
                result = result + item.lifetime
            return result / len(model.item_schedule.agents)
        else:
            return 0
