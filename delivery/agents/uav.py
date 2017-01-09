import math
import random

from mesa import Agent

from delivery.algorithms.repellentAlgorithm import Algorithm


class Uav(Agent):
    """
    A Uav is an Agent that can move. It transports Item from BaseStations to their destination
    State:
        1: idle at BaseStation,
        2: carrying an Item
        3: on the way to a Base Station
        4: battery low
        5: charging
        6: stranded without battery life left
    """
    def __init__(self, model, pos, id, max_battery, battery_low, base_station):
        # TODO: Why do we have the model here? This should not be available
        self.model = model
        self.pos = pos
        self.id = id
        self.destination = None
        self.walk = []
        self.item = None
        self.state = 1
        # Battery
        self.current_charge = max_battery
        self.max_battery = max_battery
        self.battery_low = battery_low
        # Base Stations
        self.base_station = base_station
        # Delivery
        self.initial_delivery_distance = 0
        self.initial_delivery_distance_divided_by_average_walk_length = []
        self.algorithm = Algorithm(self)
        self.last_repellent = 2
        # ??
        self.real_walk = []
        self.walk_lengths = []
        self.obstacle_list = []
        pass

    def step(self):
        """
        Advance the Uav one step
        """
        # If the UAV is IDLE at a Base Station
        if self.state == 1:
            if self.base_station.pos == self.pos:
                # ... try to pick up an Item if one is available
                self.pick_up_item(self.base_station.get_item())
                return
            # ... otherwise wait for an Item
        # If the UAV is carrying an Item
        elif self.state == 2:
            # ... and has reached the destination
            if self.pos == self.destination:
                self.deliver_item()
            # ... otherwise keep delivering the Item
            self.algorithm.run()
        # If the UAV is on the way to a Base Station
        elif self.state == 3:
            # ... and has reached the Base Stations
            if self.pos == self.destination:
                # ... update the state
                self.arrive_at_base_station(idle=True, charge=True)
            # .. otherwise keep finding the Base Station
            else:
                self.algorithm.run()
        # If the UAV is low on battery life
        elif self.state == 4:
            # ... and has reached the Base Stations
            if self.pos == self.destination:
                # ... update the state
                self.arrive_at_base_station(charge=True)
            # .. otherwise keep finding the Base Station
            else:
                self.algorithm.run()
        # If the UAV is charging the battery at a Base Station
        elif self.state == 5 or self.state == 1:
            # ... charge the battery
            self.charge_battery()
        # If the UAV has no battery life left
        elif self.state == 6:
            # ... do nothing ... RIP
            return

        # Decrease battery life
        if self.state == 2 or self.state == 3 or self.state == 4:
            # TODO: Make this configurable
            self.current_charge -= 1
            # ... and check the status
            self.check_battery()

        return

    def charge_battery(self):
        """
        Charge the battery of a UAV
        """
        # TODO: Make this configurable
        self.current_charge += 10
        print(' Agent: {}  charges battery. Battery: {}'.format(self.id, self.current_charge))
        # If the battery is fully charged
        if self.current_charge >= self.max_battery:
            self.current_charge = self.max_battery
            print(' Agent: {} is fully charged'.format(self.id))
            # If the UAV does not carry an Item
            if self.item is None:
                # ... IDLE at the Base Station in the next step
                self.state = 1
            # Otherwise resume the delivery
            else:
                self.state = 2
                self.destination = self.item.destination

    def check_battery(self):
        """
        Check if the current charge of the battery is suficciant to carry on, otherwise
        the UAV heads towards the closest Base Station for charging
        """
        if self.current_charge < self.battery_low:
            self.state = 4
            self.destination = self.base_station.get_pos()
            print(' Agent: {}  has low Battery. going to Base Station: {}'.format(self.id, self.destination))
        if self.current_charge <= 0:
            self.state = 6
            print(' Agent: {}  has no Battery life left.'.format(self.id))

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
            self.initial_delivery_distance = self.get_euclidean_distance(self.pos, self.destination)
            print(' Agent: {} Received Item {}. Delivering to {}. Distance to Destination: {}. Battery: {}'.format(self.id,
                                                                                                                   item.id,
                                                                                                                   self.destination,
                                                                                                                   self.get_euclidean_distance(
                                                                                                                       self.pos,
                                                                                                                       self.destination),
                                                                                                                   self.current_charge))

    def deliver_item(self):
        """
        The Uav delivers an Item
        """
        # Fly back to Base Station after delivering the Item
        self.destination = self.base_station.get_pos()
        print(' Agent: {}  Delivered Item {} to {}. Flying back to base at: {}. Battery: {}'.format(self.id, self.item.id, self.pos,
                                                                                                    self.destination, self.current_charge))
        print(' Agent: {}  Needed {} steps and took this walk: {}'.format(self.id, len(self.walk) - 1,
                                                                          self.walk))
        # Deliver the Item
        self.item.deliver(self.model.perceived_world_grid)
        # Remove item from model's item_schedule
        self.model.item_schedule.remove(self.item)
        self.item = None
        # Clear out the previous walk
        self.walk = []
        self.walk_lengths.append(len(self.real_walk))
        self.initial_delivery_distance_divided_by_average_walk_length.append(len(self.real_walk) / self.initial_delivery_distance)
        self.initial_delivery_distance = []
        self.real_walk = []
        # Update state
        self.state = 3
        # Notify model that a delivery was made
        # TODO: Make this more beautiful!
        self.model.number_of_delivered_items += 1

    def arrive_at_base_station(self, idle=False, charge=False):
        """
        The UAV arrives at the Base Station
        :param idle: Indicator if the UAV should be IDLE in the next step
        :param charge: Indicator if the UAV should be charging in the next step
        :return:
        """
        print(' Agent: {}  Arrived at BaseStation {}. Battery: {} '.format(self.id, self.destination, self.current_charge))
        # Update state
        if charge:
            self.state = 5
        if idle:
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
        return self.walk_lengths

    def get_initial_delivery_distance_divided_by_average_walk_length(self):
        return self.initial_delivery_distance_divided_by_average_walk_length
