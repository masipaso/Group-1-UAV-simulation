import configparser
import random
from random import randint

from mesa import Model
from mesa.datacollection import DataCollector

from shape_model.agents.baseStation import BaseStation
from shape_model.agents.obstacle import Obstacle
from shape_model.agents.uav import UAV
from shape_model.grid.multi_grids import TwoMultiGrid
from shape_model.schedule.schedule import RandomActivationByType


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

        # Set parameters
        self.schedule = RandomActivationByType(self)
        self.width = config.getint('Grid', 'width')
        self.height = config.getint('Grid', 'height')
        self.number_of_base_stations = config.getint('Basestation', 'number_of_base_stations')
        self.number_of_uavs = config.getint('Uav', 'number_of_uavs')

        # Add a grid that is used to visualize the 'actual' world
        self.grid = TwoMultiGrid(self.height, self.width, torus=False)
        # Add a grid that is used to visualize the perceived world
        self.perceived_world_grid = TwoMultiGrid(self.height, self.width, torus=False)

        # Add data collector
        self.datacollector = DataCollector(
            {
                "UAVS": lambda m: m.schedule.get_type_count(UAV),
                "Items (Waiting)": self.compute_number_of_items,
                "Items (Picked up)": self.compute_number_of_picked_up_items,
                "Items (Delivered)": self.compute_number_of_delivered_items,
             }
        )

        # Store all repellents
        # TODO: solve this in a better way!
        self.repellents = []

        # In the beginning there are no delivered Items
        self.number_of_delivered_items = 0

        # Populate the grid with obstacles and stuff
        self.populate_grid()

        self.running = True

    def step(self):
        """

        """
        self.schedule.step()
        self.datacollector.collect(self)

    def populate_grid(self):

        """
        Populate the grid with obstacles, base stations and uavs
        """

        # Create Obstacles
        for j in range(1, self.height, 5):
            for i in range(1, self.width, 5):
                form = randint(1, 1)
                if form == 1:
                    self.make_l(i, j)
                if form == 2:
                    self.make_u(i, j)
                if form == 3:
                    self.make_square(i, j)

        # Create BaseStations
        for i in range(self.number_of_base_stations):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            x = 5
            y = 5
            # while self.grid.is_cell_empty((x, y)):
            #    x = random.randrange(self.width)
            #    y = random.randrange(self.height)
            base_station = BaseStation(model=self, pos=(x, y), id=i)
            self.grid.place_agent(base_station, (x, y))
            self.perceived_world_grid.place_agent(base_station, (x, y))
            self.schedule.add(base_station)

        # Create UAV's
        for i in range(self.number_of_uavs):
            # Select one base station randomly
            start_base_station = random.choice(self.schedule.agents_by_type[BaseStation])
            # Create the uav
            uav = UAV(self, pos=start_base_station.pos, id=i, base_stations=self.schedule.agents_by_type[BaseStation])
            # Place the uav at the position of the selected base station
            self.grid.place_agent(uav, start_base_station.pos)
            self.perceived_world_grid.place_agent(uav, start_base_station.pos)
            # x = random.randrange(self.width)
            # y = random.randrange(self.height)
            # while not self.grid.is_cell_empty((x, y)):
            #     x = random.randrange(self.width)
            #     y = random.randrange(self.height)
            # uav.setDestination((x, y))
            self.schedule.add(uav)

    def make_l(self, i, j):
        """
        Create a l-shaped obstacle at a defined position
        :param i:
        :param j:
        """
        obstacle = Obstacle(self,(i, j))
        self.grid.place_agent(obstacle, (i, j))

        for x in range(1, 4, 1):
            obstacle = Obstacle(self, (i, j + x))
            self.grid.place_agent(obstacle, (i, j + x))

        for y in range(1, 4, 1):
            obstacle = Obstacle(self, (i + y, j))
            self.grid.place_agent(obstacle, (i + y, j))

    def make_u(self,i , j):
        """
        Create a u-shaped obstacle at a defined position
        :param i:
        :param j:
        """
        obstacle = Obstacle(self, (i, j))
        self.grid.place_agent(obstacle, (i, j))

        for x in range(1, 4, 1):
            obstacle = Obstacle(self, (i, j + x))
            self.grid.place_agent(obstacle, (i, j + x))
            obstacle = Obstacle(self, (i + 3, j + x))
            self.grid.place_agent(obstacle, (i + 3, j + x))

        for y in range(1, 4, 1):
            obstacle = Obstacle(self, (i + y, j))
            self.grid.place_agent(obstacle, (i + y, j))

    def make_square(self, i, j):
        """
        Create a square-shaped obstacle at a defined position
        :param i:
        :param j:
        """

        for x in range(1, 4, 1):
            obstacle = Obstacle(self, (i, j + x))
            self.grid.place_agent(obstacle, (i, j + x))
            obstacle = Obstacle(self, (i+3, j + x))
            self.grid.place_agent(obstacle, (i +3 , j + x))

        for y in range(0, 4, 1):
            obstacle = Obstacle(self, (i + y, j))
            self.grid.place_agent(obstacle, (i + y, j))

        obstacle = Obstacle(self, (i + 1, j + 3))
        self.grid.place_agent(obstacle, (i + 1, j + 3))
        obstacle = Obstacle(self, (i + 2, j + 3))
        self.grid.place_agent(obstacle, (i + 2, j + 3))

    def compute_number_of_items(self, model):
        """
        Compute the number of items that are currently in a base station
        :return: number of items located in all base stations
        """
        number_of_items = 0
        for base_station in model.schedule.agents_by_type[BaseStation]:
            number_of_items += base_station.get_number_of_items()
        return  number_of_items

    def compute_number_of_picked_up_items(self, model):
        """
        Compute the number of items that are currently delivered
        :return: number of items that are currently delivered
        """
        number_of_picked_up_items = 0
        for base_station in model.schedule.agents_by_type[BaseStation]:
            number_of_picked_up_items += base_station.get_number_of_items(picked_up=True)
        return number_of_picked_up_items

    def compute_number_of_delivered_items(self, model):
        """
        Computer the number of items that are already delivered
        :return: number of items that are already delivered
        """
        return model.number_of_delivered_items
