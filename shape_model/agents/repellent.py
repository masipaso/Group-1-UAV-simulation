from mesa import Agent


class Repellent(Agent):
    """
    A Repellent is an indicator that the cell in which the repellent is placed is not a good choice to move to
    """
    def __init__(self, model, pos):
        self.model = model
        self.pos = pos
        # TODO: Make this configurable
        self.strength = 100.00
        pass

    def step(self):
        self.weaken()
        if self.strength <= 0:
            self.model.perceived_world_grid._remove_agent(self.pos, self)
        pass

    def weaken(self):
        # TODO: Make this configurable
        decrease = -1.1
        self.strength *= decrease

    def strengthen(self):
        # TODO: Make this configurable
        increase = 1.1
        self.strength *= increase

    def get_position(self):
        """
        Get the position of a Repellent
        :return: position of the agent as a tuple of coordinates
        """
        return self.pos
