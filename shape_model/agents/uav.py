import math
import random

from mesa import Agent

from shape_model.algorithms.repellentAlgorithm import Algorithm


class Uav(Agent):
    """
    A Uav is an Agent that can move. It transports Item from BaseStations to their destination
    State: 1: idle at BaseStation, 2: carrying an Item, 3: on the way to a BaseStation, 4: ....
    """
    def __init__(self, model, pos, id, base_stations=[]):
        self.model = model
        self.pos = pos
        self.id = id
        self.destination = None
        self.walk = []
        self.item = None
        self.state = 1
        self.base_stations = base_stations
        #self.algorithm = Algorithm(self)
        self.initial_delivery_distance = 0
        self.initial_delivery_distance_divided_by_average_walk_length = []
        self.algorithm = Algorithm(self)
        self.last_repellent = 2
        self.realWalk = []
        self.walklengths= []
        self.obstacleList = []
        pass

    def step(self):
        """
        Advance the Uav one step
        """
        # If the Uav arrived at a BaseStation
        if self.state == 3 and self.get_euclidean_distance(self.pos, self.destination) == 0:
            self.arrive_at_base_station()
        # If the Uav is on the way to a BaseStation
        elif self.state == 3:
            # ... keep running
            self.algorithm.run()
        # If the Uav is idle at a BaseStation
        elif self.state == 1:
            # Iterate over all BaseStations
            for base in self.base_stations:
                # If the Uav is at a BaseStation
                if base.pos == self.pos:
                    # ... try to pick up an Item
                    self.pick_up_item(base.pickup_item())
                    return
            # ... finish this step (wait for an Item or wait to leave with an Item)
            return
        # If the Uav is delivering an Item and is at the destination
        elif self.state == 2 and self.get_euclidean_distance(self.pos, self.destination) == 0:
            # ... deliver the Item
            self.deliver_item()
            return
        # If the Uav is delivering an Item but is not at the destination
        elif self.state == 2:
            # ... keep finding the destination
            self.algorithm.run()
        else:
            return

    @staticmethod
    def get_euclidean_distance(pos1, pos2):
        """
        Calculate Euclidean distance
        :param pos1: tuple of coordinates
        :param pos2: tuple of coordinates
        :return: the euclidean distance between both positions
        """
        if pos1 == pos2:
            return 0
        else:
            p0d0 = math.pow(pos1[0] - pos2[0], 2)
            p1d1 = math.pow(pos1[1] - pos2[1], 2)
            return math.sqrt(p0d0 + p1d1)

    def pick_up_item(self, item):
        """
        The Uav picks up an Item at a BaseStation if the Uav is on the way to the BaseStation
        :param item: the Item that is picked up
        """
        if self.state == 1 and item is not None:
            self.item = item
            # Set the new destination
            self.destination = self.item.get_destination()
            # Update state
            self.state = 2
            # Clear out the previous walk
            self.walk = []
            self.initial_delivery_distance = self.get_euclidean_distance(self.pos,self.destination)
            print(' Agent: {} Received Item {}. Delivering to {}. Distance to Destination: {}'.format(self.id, item.id,
                                                                                                      self.destination,
                                                                                                      self.get_euclidean_distance(
                                                                                                        self.pos,
                                                                                                        self.destination)))

    def deliver_item(self):
        """
        The Uav delivers an Item
        """
        target_base_station = random.choice(self.base_stations)
        self.destination = target_base_station.pos
        print(' Agent: {}  Delivered Item {} to {}. Flying back to base at: {}'.format(self.id, self.item.id, self.pos,
                                                                                       self.destination))
        print(' Agent: {} Walk taken: {}, Length: {}'.format(self.id,self.realWalk,len(self.realWalk)))
        # Deliver the Item
        self.item.deliver(self.model.perceived_world_grid)
        self.item = None
        # Clear out the previous walk
        self.walk = []
        self.walklengths.append(len(self.realWalk))
        self.initial_delivery_distance_divided_by_average_walk_length.append(len(self.realWalk)/self.initial_delivery_distance)
        self.initial_delivery_distance = []
        self.realWalk = []
        # Update state
        self.state = 3
        # Notify model that a delivery was made
        # TODO: Make this more beautiful!
        self.model.number_of_delivered_items += 1

    def arrive_at_base_station(self):
        """
        The Uav arrives at the BaseStation
        """
        print(' Agent: {}  Arrived at BaseStation {} '.format(self.id, self.destination))
        # Update state
        self.state = 1

    def move_to(self, pos):
        """
        Move an Uav to a position
        :param pos: tuple of coordinates where the uav should move to
        """
        # Move the agent on both grids
        self.model.grid.move_agent(self, pos)
        self.model.perceived_world_grid.move_agent(self, pos)
        # Update the position on the agent, because the move_agent function does not do that for us!
        self.pos = pos

    def get_walk_lengths(self):
        return self.walklengths

    def get_initial_delivery_distance_divided_by_average_walk_length(self):
        return self.initial_delivery_distance_divided_by_average_walk_length
