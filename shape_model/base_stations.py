from mesa import Agent
import random
from random import randint
from shape_model.items import Item

class BaseStation(Agent):
    '''
    A BaseStation is an Agent that cannot move
    '''
    def __init__(self, model,pos,id):
        self.model = model
        self.pos = pos
        self.id = id
        self.noItems = 0
        self.items = []
        pass

    def step(self):
        if randint(1, 10) <= 3:
            x = random.randrange(self.model.width)
            y = random.randrange(self.model.height)
            while not self.model.grid.is_cell_empty((x, y)):
                x = random.randrange(self.model.width)
                y = random.randrange(self.model.height)
            itemdestination = (x,y)
            self.noItems += 1
            item = Item(destination=itemdestination, priority=0,id=str(self.id) + "_" + str(self.noItems))
            self.items.append(item)
            print("Created item {}, destination: {}, priority:{}".format(item.id, item.destination,item.priority))


    def pickupItem(self):
        if not len(self.items)== 0:
            return random.choice(self.items)
        else:
            return None

