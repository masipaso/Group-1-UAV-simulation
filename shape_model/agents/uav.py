import math
import random

from mesa import Agent

from shape_model.algorithms_jan import MyAlgorithm


class UAV(Agent):
    '''
    A UAV is an Agent that can move. It transports goods
    State: 1: empty, 2: carrying an item, 3: , 4: ....
    '''
    def __init__(self, model, pos, id, base_stations=[]):
        self.model = model
        self.pos = pos
        self.id= id
        self.destination = pos
        self.walk = []
        self.pastDistances = []
        self.item = None
        self.state = 1
        self.base_stations = base_stations
        self.algorithm = MyAlgorithm(self)
        self.last_repellent = 2
        pass

    def step(self):
        """
        Advance the UAV one step
        """
        if self.state == 1:
            for base in self.base_stations:
                if base.pos == self.pos:
                    self.assign_item(base.pickupItem())
                    return
            if self.item is None:
                self.algorithm.run()
                return
        elif self.state == 2 and self.get_euclidean_distance(self.pos,self.destination) == 0:
            self.deliver()
            return
        elif self.state == 2:
            self.algorithm.run()

    def set_destination(self, destination):
        self.destination = destination
        initial_distance = self.get_euclidean_distance(self.pos, self.destination)
        self.walk.append((self.pos, initial_distance))

    def get_euclidean_distance(self,pos1,pos2):
        """
        Calculate Euclidean distance
        :param pos1: tuple of coordinates
        :param pos2: tuple of coordinates
        :return: the euclidean distance between both positions
        """
        if pos1 == pos2:
            return 0
        else:
            p0d0= math.pow(pos1[0]-pos2[0],2)
            p1d1= math.pow(pos1[1]-pos2[1],2)
            return math.sqrt(p0d0+p1d1)

    def assign_item(self, item):
        if self.state == 1 and item != None:
            self.item = item
            self.destination = self.item.getDestination()
            print(' Agent: {}  Received Item {}. Delivering to {}. Distance to Destination: {}'.format(self.id, item.id,self.destination, self.get_euclidean_distance(self.pos,self.destination)))
            self.state = 2
            self.walk = []

    def deliver(self):
        target_base_station = random.choice(self.base_stations)
        self.destination = target_base_station.pos
        print(' Agent: {}  Delivered Item {} to {}. Flying back to base at: {}'.format(self.id, self.item.id, self.pos,self.destination))
        self.model.perceived_world_grid._remove_agent(self.pos, self.item) #disregard the _
        self.item = None
        self.walk = []
        self.state = 1
        # Notify model that a delivery was made
        self.model.number_of_delivered_items = + 1

    def get_position(self):
        """
        Get the position of a UAV
        :return: position of the agent as a tuple of coordinates
        """
        return self.pos

    def move_to(self, pos):
        # Move the agent on both grids
        self.model.grid.move_agent(self, pos)
        self.model.perceived_world_grid.move_agent(self, pos)
        # Update the position on the agent, because the move_agent function does not do that for us!
        self.pos = pos
