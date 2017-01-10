import random
import configparser

from mesa import Agent

from delivery.agents.item import Item


class BaseStation(Agent):
    """
    A BaseStation is an Agent that cannot move
    """
    def __init__(self, model, pos, id, center, range_of_base_station):
        """

        :param model: worldmodel
        :param pos: position of the base station
        :param id: unique id of the base station
        :param center: center of the assigned area in which items can spawn
        :param range_of_base_station: range of the base station
        """
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.probability_to_create_item = config.getint('Basestation','probability_to_create_item')
        self.max_item_priority = config.getint('Basestation','max_item_priority')
        self.range_of_base_station = range_of_base_station

        self.model = model
        self.pos = pos
        self.id = id
        self.items = []
        self.picked_up_items = 0
        self.center = center
        pass

    def step(self):
        # A BaseStation creates an Item with a probability of ...
        if random.randint(1, 100) <= self.probability_to_create_item:
            self.create_item()

    def create_item(self):
        # The Item is placed at a random location inside the assigned area
        x = random.randrange(self.center[0] - self.range_of_base_station,
                             self.center[0] + self.range_of_base_station)
        y = random.randrange(self.center[1] - self.range_of_base_station,
                             self.center[1] + self.range_of_base_station)
        # ... but only if the cell is not occupied with an Obstacle or BaseStation
        # TODO: Make it possible that Items can be created at cells that already have an Item, a Uav or a Repellent
        while x >= self.model.width or y >= self.model.height or not self.model.grid.is_cell_empty((x, y)) or not self.model.perceived_world_grid.is_cell_empty((x, y)):
            x = random.randrange(self.center[0] - self.range_of_base_station,
                                 self.center[0] + self.range_of_base_station)
            y = random.randrange(self.center[1] - self.range_of_base_station,
                                 self.center[1] + self.range_of_base_station)
        item_destination = (x, y)
        # The Item receives a random priority between 1 and ...
        item_priority = random.randint(1, self.max_item_priority)
        # Create the Item
        item = Item(destination=item_destination, priority=item_priority, id=str(self.id) + "_" + str(len(self.items)))
        # Place the Item on the perceived world grid
        # TODO: Decide if the Item should be visible on the real world grid
        self.model.perceived_world_grid.place_agent(item, item_destination)
        # Add the Item to the BaseStation
        self.items.append(item)

        # Add the Item to the scheduler of the model
        self.model.item_schedule.add(item)
        print("Created item {}, destination: {}, priority: {}".format(item.id, item.destination, item.priority))
        # Sort the items by priority
        self.sort_items_by_priority()

    def get_item(self):
        """
        Assigns an Item to a Uav
        :return: either an Item, if one is available, or None
        """
        if not len(self.items) == 0:
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
        :return: tuple of coordinates
        """
        return self.pos