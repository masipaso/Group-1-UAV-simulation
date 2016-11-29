import random
import configparser

from mesa import Agent

from shape_model.agents.item import Item


class BaseStation(Agent):
    """
    A BaseStation is an Agent that cannot move
    """
    def __init__(self, model,pos,id):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.probability_to_create_item = config.getint('Basestation','probability_to_create_item')
        self.max_item_priority = config.config.getint('Basestation','max_item_priority')

        self.model = model
        self.pos = pos
        self.id = id
        self.items = []
        self.picked_up_items = 0
        pass

    def step(self):
        # A BaseStation creates an Item with a probability of ...

        if random.randint(1, 100) <= self.probability_to_create_item:
            self.create_item()

    def create_item(self):
        # The Item is placed at a random location
        x = random.randrange(self.model.width)
        y = random.randrange(self.model.height)
        # ... but only if the cell is not occupied with an Obstacle or BaseStation
        # TODO: Make it possible that Items can be created at cells that already have an Item, a Uav or a Repellent
        while not self.model.grid.is_cell_empty((x, y)) or not self.model.perceived_world_grid.is_cell_empty((x, y)):
            x = random.randrange(self.model.width)
            y = random.randrange(self.model.height)
        item_destination = (x, y)
        # The Item revceives a random priority between 1 and ...
        # TODO: Make this configurable
        max_item_priority = 10
        item_priority = random.randint(1, max_item_priority)
        # Create the Item
        item = Item(destination=item_destination, priority=item_priority, id=str(self.id) + "_" + str(len(self.items)))
        # Place the Item on the perceived world grid
        # TODO: Decide if the Item should be visible on the real world grid
        self.model.perceived_world_grid.place_agent(item, item_destination)
        # Add the Item to the BaseStation
        self.items.append(item)
        print("Created item {}, destination: {}, priority: {}".format(item.id, item.destination, item.priority))
        # Sort the items by priority
        self.sort_items_by_priority()

    def pickup_item(self):
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
