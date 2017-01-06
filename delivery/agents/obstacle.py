from mesa import Agent


class Obstacle(Agent):
    """
    An Obstacle is an Agent that cannot move
    """
    def __init__(self, model, pos):
        self.pos = pos
        pass

    def step(self):
        pass

    def get_position(self):
        """
        Get the position of an Obstacle
        :return: position of the agent as a tuple of coordinates
        """
        return self.pos
