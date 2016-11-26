import random

from mesa import Agent

from shape_model.agents.item import Item


class BaseStation(Agent):
    """
    A BaseStation is an Agent that cannot move
    """
    def __init__(self, model,pos,id):
        self.model = model
        self.pos = pos
        self.id = id
        self.items = []
        self.picked_up_items = 0
        pass

    def step(self):
        if len(self.items) < 1:
        #if random.randint(1, 10) <= 1:
            x = random.randrange(self.model.width)
            y = random.randrange(self.model.height)
            while not self.model.grid.is_cell_empty((x, y))\
                    or not self.model.perceived_world_grid.is_cell_empty((x, y)):
                x = random.randrange(self.model.width)
                y = random.randrange(self.model.height)
            item_destination = (x, y)
            item_priority = random.randint(1, 10)
            item = Item(destination=item_destination, priority=item_priority, id=str(self.id) + "_" + str(len(self.items)))
            self.items.append(item)
            self.model.perceived_world_grid.place_agent(item, item_destination)
            print("Created item {}, destination: {}, priority: {}".format(item.id, item.destination, item.priority))
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
