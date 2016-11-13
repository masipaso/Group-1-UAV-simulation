import random

from mesa.space import MultiGrid
from mesa import Model

from shape_model.obstacles import Obstacle
from shape_model.base_stations import BaseStation

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
                for x in range(0, 4, 1):
                    if x == 0 or x == 3:
                        for y in range(0, 4, 1):
                            obstacle = Obstacle(self, (x + i, y + j))
                            self.grid.place_agent(obstacle, (x + i, y + j))
                    else:
                        obstacle = Obstacle(self, (x + i, j))
                        self.grid.place_agent(obstacle, (x + i, j))
                        obstacle = Obstacle(self, (x + i, j + 3))
                        self.grid.place_agent(obstacle, (x + i, j + 3))

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
