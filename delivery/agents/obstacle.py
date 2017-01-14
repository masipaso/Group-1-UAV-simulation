from mesa import Agent

#TODO: Do we need this class??
class Obstacle(Agent):
    """
    An Obstacle is an Agent that cannot move
    :param pos: A tuple of coordinates representing the position of the Obstacle
    """
    def __init__(self, pos):
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
