import sys
import random
import configparser

from mesa import Agent

from delivery.agents.Item import Item


class BaseStation(Agent):
    """
    A BaseStation is an Agent that cannot move, is a place where UAVs can pick up Items and charge their battery.
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
        try:
            self.max_item_priority = config.getint('Base_station', 'max_item_priority', fallback=3)
        except ValueError:
            print("[Configuration] The max_item_priority is not valid.")
            sys.exit(1)

        try:
            self.max_items_per_base_station = config.getint('Base_station', 'max_items_per_base_station', fallback=10)
        except ValueError:
            print("[Configuration] The max_items_per_base_station is not valid.")
            sys.exit(1)

        self.range_of_base_station = range_of_base_station
        self.pos = pos
        self.bid = bid
        self.items = []
        self.picked_up_items = 0
        self.center = center
        self.item_counter = 0

        super().__init__(bid, model)

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
        # ... but only if the cell is empty
        while x >= self.model.width \
                or y >= self.model.height \
                or not self.model.landscape.is_cell_empty((x, y)):
            x = random.randrange(self.center[0] - self.range_of_base_station,
                                 self.center[0] + self.range_of_base_station)
            y = random.randrange(self.center[1] - self.range_of_base_station,
                                 self.center[1] + self.range_of_base_station)
        item_destination = (x, y, self.pos[2])
        # The Item receives a random priority between 1 and the defined max_item_priority
        item_priority = random.randint(1, self.max_item_priority)
        # Create the Item
        item = Item(destination=item_destination, priority=item_priority, iid=str(self.bid) + "_" + str(self.item_counter))
        self.item_counter += 1
        # Add the Item to the BaseStation
        self.items.append(item)
        # Add the Item to the scheduler of the model
        self.model.item_schedule.add(item)

    def get_item(self):
        """
        Get the Item with the highest priority
        :return: either an Item, if one is available, or None
        """
        if not len(self.items) == 0:
            # Sort items by priority
            self.sort_items_by_priority()
            item = self.items.pop()
            self.picked_up_items += 1
            return item
        else:
            return None

    def sort_items_by_priority(self):
        """
        Sort the currently available Items based on their priority
        """
        for item in self.items:
            item.pick_up_priority = item.lifetime + item.priority * 100

        self.items.sort(key=lambda item: item.pick_up_priority)

    def get_number_of_items(self, picked_up=False, by_priority=False):
        """
        Get the number of Items that are currently at the BaseStation or the number of Items that were picked up at the
        BaseStation
        :param picked_up: indicator for deciding which number should be returned
        :param by_priority: indicator for deciding what should be returned
        :return: either the currently available Items or the number of Items that were picked up at the BaseStation
        """
        if picked_up:
            return self.picked_up_items
        elif by_priority:
            items_by_priority = {}
            for priority in range(1, self.max_item_priority + 1):
                items_by_priority[priority] = 0
                for item in self.items:
                    if item.priority == priority:
                        items_by_priority[priority] += 1
            return items_by_priority
        else:
            return len(self.items)

    def get_pos(self):
        """
        Get the position of the Base Station
        :return: Triple of coordinates
        """
        return self.pos
