import random

from mesa.space import MultiGrid
from mesa import Model

from shape_model.obstacles import Obstacle
from shape_model.base_stations import BaseStation
from random import randint
class WorldModel(Model):
    '''
    Model representing the world
    '''


    def __init__(self, height=101, width=101, number_of_base_stations=7):
        '''
        Create a new WorldModel with the given parameters
        :param height:
        :param width:
        '''
        # Set parameters
        self.height = height
        self.width = width
        self.number_of_base_stations = number_of_base_stations
        self.grid = MultiGrid(self.height, self.width, torus=True)

        # Create Obstacles
        for j in range(1, self.height, 5):
            for i in range(1, self.width, 5):
                #for x in range(0, 4, 1):
                    #self.make_square(i,j)
                form = randint(1,3)
                if form == 1:
                    self.make_l(i,j)
                if form == 2:
                    self.make_square(i,j)
                if form == 3:
                    self.make_u(i,j)

        # Create BaseStations
        for i in range(self.number_of_base_stations):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            while self.grid.is_cell_empty((x, y)):
                x = random.randrange(self.width)
                y = random.randrange(self.height)
            base_station = BaseStation(self, (x, y))
            self.grid.place_agent(base_station, (x, y))

        self.running = True

    def step(self):
        pass

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
