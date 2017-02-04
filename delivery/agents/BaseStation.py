import random
import configparser

from mesa import Agent

from delivery.agents.Item import Item


class BaseStation(Agent):
    """
    A BaseStation is an Agent that cannot move
    """
    def __init__(self, model, pos, bid, center, range_of_base_station):
        """
        Initialize a BaseStation
        :param model: world model
        :param pos: position of the base station
        :param bid: unique id of the base station
        :param center: center of the assigned area in which items can spawn
        :param range_of_base_station: range of the base station
        """
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.max_item_priority = config.getint('Basestation', 'max_item_priority')
        self.max_items_per_base_station = config.getint('Basestation', 'max_items_per_base_station')
        self.range_of_base_station = range_of_base_station
        self.model = model
        self.pos = pos
        self.bid = bid
        self.items = []
        self.picked_up_items = 0
        self.center = center
        self.item_counter = 0

    def step(self):
        # A BaseStation creates an Item if max_items_per_base_station has not been reached
        if len(self.items) < self.max_items_per_base_station:
            self.create_item()

    def create_item(self):
        # The Item is placed at a random location inside the assigned area
        x = random.randrange(self.center[0] - self.range_of_base_station,
                             self.center[0] + self.range_of_base_station)
        y = random.randrange(self.center[1] - self.range_of_base_station,
                             self.center[1] + self.range_of_base_station)
        # ... but only if the cell is not occupied with an Obstacle or BaseStation
        while x >= self.model.width \
                or y >= self.model.height \
                or not self.model.landscape.is_cell_empty((x, y)):
            x = random.randrange(self.center[0] - self.range_of_base_station,
                                 self.center[0] + self.range_of_base_station)
            y = random.randrange(self.center[1] - self.range_of_base_station,
                                 self.center[1] + self.range_of_base_station)
        item_destination = (x, y, self.pos[2])
        #item_destination = (24, 82, self.pos[2])
        # The Item receives a random priority between 1 and ...
        item_priority = random.randint(1, self.max_item_priority)
        # Create the Item
        item = Item(destination=item_destination, priority=item_priority, iid=str(self.bid) + "_" + str(self.item_counter + self.picked_up_items))
        self.item_counter += 1
        # Add the Item to the BaseStation
        self.items.append(item)
        # Add the Item to the scheduler of the model
        self.model.item_schedule.add(item)
        print("Created item {}, destination: {}, priority: {}".format(item.iid, item.destination, item.priority))
        # Sort the items by priority
        self.sort_items_by_priority()

    def get_item(self):
        """
        Assigns an Item to a Uav
        :return: either an Item, if one is available, or None
        """
        if not len(self.items) == 0:
            # TODO: use pop() ?
            item = self.items[0]
            self.items.remove(item)
            self.picked_up_items += 1
            return item
        else:
            return None

    def sort_items_by_priority(self):
        """
        Sort the currently available Items based on their priority
        """
        self.items.sort(key=lambda item: item.priority)

    def get_number_of_items(self, picked_up=False):
        """
        Get the number of Items that are currently at the BaseStation or the number of Items that were picked up at the
        BaseStation
        :param picked_up: indicator for deciding which number should be returned
        :return: either the currently available Items or the number of Items that were picked up at the BaseStation
        """
        if picked_up:
            return self.picked_up_items
        return len(self.items)

    def get_pos(self):
        """
        Get the position of the Base Station
        :return: Triple of coordinates
        """
        return self.pos
