import math
from delivery.agents.repellent import Repellent
from delivery.agents.baseStation import BaseStation

from operator import itemgetter
from mesa import Agent
from delivery.grid.Multi_grid_extra import MultiGridExtra

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
    :param model: world model
    :param pos: Tuple of coordinates at which the UAV is located
    :param uid: Unique UAV identifier
    :param max_battery: The maximum charge the battery can have
    :param battery_low: The threshold at which the battery charge is considered low
    :param battery_decrease_per_step: The decrease in battery charge per step
    :param battery_increase_per_step: The increase in battery charge while charging per step
    :param base_station: The 'home' BaseStation
    """
    def __init__(self, model, pos, uid, max_battery, battery_low, battery_decrease_per_step, battery_increase_per_step,
                 base_station):
        # TODO: Why do we have the model here? This should not be available
        self.model = model
        self.pos = pos
        self.uid = uid
        self.destination = None
        self.walk = []
        self.item = None
        self.state = 1

        # Create a UAV-specific grid for repellents and item destinations
        self.perceived_grid = MultiGridExtra(height=self.model.grid.height, width=self.model.grid.width,
                                             torus=self.model.grid.torus)

        # Battery
        self.current_charge = max_battery
        self.max_battery = max_battery
        self.battery_low = battery_low
        self.battery_decrease_per_step = battery_decrease_per_step
        self.battery_increase_per_step = battery_increase_per_step
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
            self.find_uavs_close()
            self.algorithm.run()
        # If the UAV is on the way to a Base Station
        elif self.state == 3:
            # ... and has reached the Base Stations
            if self.pos == self.destination:
                # ... update the state
                self.arrive_at_base_station(idle=True, charge=True)
            # .. otherwise keep finding the Base Station
            else:
                self.find_uavs_close()
                self.algorithm.run()
        # If the UAV is low on battery life
        elif self.state == 4:
            # ... and has reached the Base Stations
            if self.pos == self.destination:
                # ... update the state
                self.arrive_at_base_station(charge=True)
            # .. otherwise keep finding the Base Station
            else:
                self.find_uavs_close()
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
            self.current_charge -= self.battery_decrease_per_step
            # ... and check the status
            self.check_battery()

        return

    def charge_battery(self):
        """
        Charge the battery of a UAV
        """
        self.current_charge += self.battery_increase_per_step
        print(' Agent: {}  charges battery. Battery: {}'.format(self.uid, self.current_charge))
        # If the battery is fully charged
        if self.current_charge >= self.max_battery:
            self.current_charge = self.max_battery
            print(' Agent: {} is fully charged'.format(self.uid))
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
        Check if the current charge of the battery is sufficient to carry on, otherwise
        the UAV heads towards the closest Base Station for charging
        """
        if self.current_charge < self.battery_low:
            self.state = 4
            self.destination = self.get_nearest_base_station()
            print(' Agent: {}  has low Battery. going to Base Station: {}'.format(self.uid, self.destination))
        if self.current_charge <= 0:
            self.state = 6
            print(' Agent: {}  has no Battery life left.'.format(self.uid))

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
            # Place the Item on the perceived grid of the UAV
            self.perceived_grid.place_agent(pos=item.destination, agent=item)
            # Update state
            self.state = 2
            # Clear out the previous walk
            self.walk = []
            self.initial_delivery_distance = self.get_euclidean_distance(self.pos, self.destination)
            print(' Agent: {} Received Item {}. Delivering to {}. Distance to Destination: {}. Battery: {}'
                  .format(self.uid, item.iid, self.destination, self.get_euclidean_distance(self.pos, self.destination),
                          self.current_charge))

    def deliver_item(self):
        """
        The Uav delivers an Item
        """
        # Fly back to Base Station after delivering the Item
        self.destination = self.choose_base_station_to_pick_up_item_from()
        print(' Agent: {}  Delivered Item {} to {}. Flying back to base at: {}. Battery: {}'
              .format(self.uid, self.item.iid, self.pos, self.destination, self.current_charge))
        print(' Agent: {}  Needed {} steps and took this walk: {}'
              .format(self.uid, len(self.walk) - 1, self.walk))
        # Deliver the Item
        self.item.deliver(self.perceived_grid)
        # Remove item from model's item_schedule
        self.model.item_schedule.remove(self.item)
        self.item = None
        # Clear out the previous walk
        self.walk = []
        self.walk_lengths.append(len(self.real_walk))
        self.initial_delivery_distance_divided_by_average_walk_length.append(len(self.real_walk)
                                                                             / self.initial_delivery_distance)
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
        print(' Agent: {}  Arrived at BaseStation {}. Battery: {} '
              .format(self.uid, self.destination, self.current_charge))
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

    # TODO: @Dominik what are walk lengths?
    def get_walk_lengths(self):
        """
        Get the lengths of the walks
        :return: Length of the walks
        """
        return self.walk_lengths

    # TODO: @Dominik please write a method definition (and describe what this does)
    def get_initial_delivery_distance_divided_by_average_walk_length(self):
        return self.initial_delivery_distance_divided_by_average_walk_length

    def find_uavs_close(self):
        """
        Locate UAVs that are close and exchange grids
        """
        neighborhood = self.model.grid.get_neighborhood(pos=self.pos,moore=True,include_center=False,radius=2)
        # The worst loop ever!
        if self.model.steps <= 50:
            return
        for pos in neighborhood:
            for obj in self.model.grid.get_cell_list_contents(pos):
                if isinstance(obj ,Uav) and obj is not self:
                    print("Agent {} and {} exchanging grid".format(self.uid, obj.uid))
                    other_grid = obj.perceived_grid

                    # Actual program logic for grid exchange: finding repellents on other grid and check if I update mine
                    # Very slow and random selection of neighboring UAV
                    for x in range(0, other_grid.width - 1):
                        for y in range(0, other_grid.height - 1):
                            other_repellent = other_grid.get_repellent_on((x, y))
                            my_repellent = self.perceived_grid.get_repellent_on((x, y))
                            if other_repellent is not None:
                                if my_repellent is None:

                                    # Placing a new repellent if I do not know this one already
                                    new_repellent = Repellent(self.model, (x, y), self.perceived_grid)
                                    new_repellent.strength = other_repellent.strength
                                    self.perceived_grid.place_agent(agent=new_repellent, pos=(x, y))

                                else:
                                    # Repellent already placed at my own grid
                                    # TODO: Make second part of if clause more intelligent aka avoid exchanging grid if already exchanged upto n steps ago.
                                    # TODO: So actually never get here in that case
                                    if my_repellent.get_last_updated_at() < other_repellent.get_last_updated_at() and my_repellent.strength is not other_repellent.strength:
                                        print("Agent {} updates repellent from Agent {}. Old strength: {}, New: {}".format(self.uid, obj.uid, my_repellent.strength, other_repellent.strength))
                                        my_repellent.strength = other_repellent.strength
                                        my_repellent.last_updated_at = self.model.steps

    def get_nearest_base_station(self):
        """
        Get the BaseStation that is closest to the UAV
        :return: The nearest BaseStation
        """
        # Based on euclidean distance, select closest baseStation
        base_stations = self.model.schedule.agents_by_type[BaseStation]
        base_stations_by_distance = []
        for station in base_stations:
            base_stations_by_distance.append((station.pos, self.get_euclidean_distance(self.pos, station.pos)))
            base_stations_by_distance.sort(key=lambda tup: tup[1])
        return base_stations_by_distance.pop(0)[0]

    def choose_base_station_to_pick_up_item_from(self):
        """
        Choose a BaseStation to pick up an Item
        :return: The nearest BaseStations
        """
        # Based on number of items and distance of BaseStation, select next BaseStation to pick up items from
        # TODO: This should be decentralized in the next step!
        base_stations = self.model.schedule.agents_by_type[BaseStation]
        base_stations_by_distance = []
        for station in base_stations:
            base_stations_by_distance.append((station.pos, self.get_euclidean_distance(self.pos, station.pos),
                                              len(station.items)))
            sorted(base_stations_by_distance,  key=itemgetter(2,1))
        print("List of BaseStations: {}".format(base_stations_by_distance))
        return base_stations_by_distance.pop(0)[0]