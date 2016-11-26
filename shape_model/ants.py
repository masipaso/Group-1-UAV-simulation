from mesa import Agent


class Repellent(Agent):
    '''
    An Obstacle is an Agent that cannot move
    '''
    def __init__(self, model,pos):
        self.model = model
        self.pos = pos
        pass

    def step(self):
        pass

    def get_position(self):
        """
        Get the position of a Repellent
        :return: position of the agent as a tuple of coordinates
        """
        return self.pos

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

    def get_position(self):
        """
        Get the position of a Pheromone
        :return: position of the agent as a tuple of coordinates
        """
        return self.pos