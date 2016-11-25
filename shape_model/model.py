import random

from mesa.space import MultiGrid
from mesa import Model
from mesa.datacollection import DataCollector

from shape_model.obstacles import Obstacle
from shape_model.base_stations import BaseStation
from shape_model.uavs import UAV
from random import randint

from shape_model.schedule import RandomActivationByType

class WorldModel(Model):
    '''
    Model representing the world
    '''


    def __init__(self, height=101, width=101, number_of_base_stations=6, number_of_uavs=8):
        '''
        Create a new WorldModel with the given parameters
        :param height:
        :param width:
        '''
        # Set parameters
        self.schedule = RandomActivationByType(self)
        self.height = height
        self.width = width
        self.number_of_base_stations = number_of_base_stations
        self.number_of_uavs = number_of_uavs
        self.number_of_delivered_items = 0
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector(
            {
                "UAVS": lambda m: m.schedule.get_type_count(UAV),
                "Items (Waiting)": self.compute_number_of_items,
                "Items (Picked up)": self.compute_number_of_picked_up_items,
                "Items (Delivered)": self.compute_number_of_delivered_items,
             }
        )
        self.repellents = []

        # Create Obstacles
        for j in range(1, self.height, 5):
            for i in range(1, self.width, 5):
                form = randint(1,1)
                if form == 1:
                    self.make_l(i,j)
                if form == 2:
                    self.make_u(i,j)
                if form == 3:
                    self.make_square(i,j)

        # Create BaseStations
        for i in range(self.number_of_base_stations):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            while self.grid.is_cell_empty((x, y)):
                x = random.randrange(self.width)
                y = random.randrange(self.height)
            base_station = BaseStation(model=self, pos=(x, y), id=i)
            self.grid.place_agent(base_station, (x, y))
            self.schedule.add(base_station)

        # Create UAV's
        for i in range(self.number_of_uavs):
            start_baseStation = random.choice(self.schedule.agents_by_type[BaseStation])
            uav = UAV(self, pos=start_baseStation.pos,id=i,baseStations=self.schedule.agents_by_type[BaseStation])
            self.grid.place_agent(uav, start_baseStation.pos)
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            while not self.grid.is_cell_empty((x, y)):
                x = random.randrange(self.width)
                y = random.randrange(self.height)
            uav.setDestination((x,y))
            self.schedule.add(uav)

        self.running = True


    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def make_l(self,i,j):
        obstacle = Obstacle(self,(i,j))
        self.grid.place_agent(obstacle,(i,j))

        for x in range(1,4,1):
            obstacle = Obstacle(self, (i, j+x))
            self.grid.place_agent(obstacle, (i, j+x))

        for y in range(1,4,1):
            obstacle = Obstacle(self, (i+y, j ))
            self.grid.place_agent(obstacle, (i+y, j ))

    def make_u(self,i,j):

        obstacle = Obstacle(self,(i,j))
        self.grid.place_agent(obstacle,(i,j))

        for x in range(1,4,1):
            obstacle = Obstacle(self, (i, j+x))
            self.grid.place_agent(obstacle, (i, j+x))
            obstacle = Obstacle(self, (i+3, j + x))
            self.grid.place_agent(obstacle, (i+3, j + x))

        for y in range(1,4,1):
            obstacle = Obstacle(self, (i+y, j ))
            self.grid.place_agent(obstacle, (i+y, j ))

    def make_square(self,i,j):

        for x in range(1,4,1):
            obstacle = Obstacle(self, (i, j+x))
            self.grid.place_agent(obstacle, (i, j+x))
            obstacle = Obstacle(self, (i+3, j + x))
            self.grid.place_agent(obstacle, (i+3, j + x))

        for y in range(0, 4, 1):
            obstacle = Obstacle(self, (i + y, j))
            self.grid.place_agent(obstacle, (i + y, j))

        obstacle = Obstacle(self, (i+1 , j+3))
        self.grid.place_agent(obstacle, (i+1, j+3))
        obstacle = Obstacle(self, (i + 2, j + 3))
        self.grid.place_agent(obstacle, (i + 2, j + 3))

    def compute_number_of_items(self, model):
        number_of_items = 0
        for base_station in model.schedule.agents_by_type[BaseStation]:
            number_of_items += base_station.get_number_of_items()
        return  number_of_items

    def compute_number_of_picked_up_items(self, model):
        number_of_picked_up_items = 0
        for base_station in model.schedule.agents_by_type[BaseStation]:
            number_of_picked_up_items += base_station.get_number_of_items(picked_up=True)
        return number_of_picked_up_items

    def compute_number_of_delivered_items(self, model):
        return model.number_of_delivered_items
