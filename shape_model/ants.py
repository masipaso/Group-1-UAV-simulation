from mesa import Agent


class Repellent(Agent):
    '''
    An Obstacle is an Agent that cannot move
    '''
    def __init__(self, model,pos):
        pass

    def step(self):
        pass


class Pheromones(Agent):
    '''
    An Obstacle is an Agent that cannot move
    '''
    def __init__(self, model,pos):
        self.model = model
        self.pos = pos
        self.model.appendPheromones(self)
        self.strength=100.0
        pass

    def step(self):
        self.strength = self.strength - 1
        if self.strength <= 0:
            self.model.removePhereomones(self)
        pass

    def strengthen(self):
        self.strength = self.strength*1.1