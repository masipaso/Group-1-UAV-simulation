import configparser
import random
from random import randint

from mesa import Model
from mesa.datacollection import DataCollector

from shape_model.agents.baseStation import BaseStation
from shape_model.agents.obstacle import Obstacle
from shape_model.agents.uav import Uav
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

        # Configure schedule for Uavs and BaseStations
        self.schedule = RandomActivationByType(self)
        # Configure schedule for Repellents
        self.repellent_schedule = RandomActivationByType(self)
        # Set parameters
        self.width = config.getint('Grid', 'width')
        self.height = config.getint('Grid', 'height')
        self.number_of_base_stations = config.getint('Basestation', 'number_of_base_stations')
        self.number_of_uavs = config.getint('Uav', 'number_of_uavs')
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
             }
        )

        # In the beginning there are no delivered Items
        self.number_of_delivered_items = 0

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
            self.create_base_station(i)

        # Create Uavs
        for i in range(self.number_of_uavs):
            self.create_uav(i)

    def create_uav(self, id):
        """
        Create a Uav
        :param id: unique identifier of the Uav
        """
        # Select one base station randomly
        start_base_station = random.choice(self.schedule.agents_by_type[BaseStation])
        # Create the uav
        uav = Uav(self, pos=start_base_station.pos, id=id, base_stations=self.schedule.agents_by_type[BaseStation])
        # Place the uav on the grids
        self.grid.place_agent(uav, start_base_station.pos)
        self.perceived_world_grid.place_agent(uav, start_base_station.pos)
        # Add the Uav to the schedule
        self.schedule.add(uav)

    def create_base_station(self, id):
        """
        Create a BaseStation at a random location
        :param id: unique identifier of the BaseStation
        """
        # Select a random location
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        # ... if there is no Obstacle on that position, choose another location
        while self.grid.is_cell_empty((x, y)):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
        # Create the BaseStation
        base_station = BaseStation(model=self, pos=(x, y), id=id)
        # Place the BaseStation on the grids
        self.grid.place_agent(base_station, (x, y))
        self.perceived_world_grid.place_agent(base_station, (x, y))
        # Add the BaseStation to the schedule
        self.schedule.add(base_station)

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
        sum_walks = 0

        for uav in model.schedule.agents_by_type[Uav]:
            for elem in uav.get_walk_lengths():
                average_walks.append(elem)
        if len(average_walks)>0:
            return sum(average_walks)/len(average_walks)
        else: return 0


