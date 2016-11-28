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
        self.model.repellent_schedule.add(self)
        pass

    def step(self):
        """
        Advance the Repellent on step
        """
        # Weaken the Repellent
        self.weaken()
        # If the strength of the Repellent is below 0
        if self.strength <= 0:
            # ... Remove it from the grid
            self.model.perceived_world_grid._remove_agent(self.pos, self)
            # ... and from the schedule
            self.model.repellent_schedule.remove(self)
        pass

    def weaken(self):
        """
        Weaken a Repellents strength
        """
        # TODO: Make this configurable
        decrease = 0.25
        self.strength -= decrease

    def strengthen(self):
        """
        Reset a Repellents strength
        """
        # TODO: Make this configurable
        # TODO: Should we increase this by a number instead of setting it to a fixed value?
        self.strength = 100.00

    def get_position(self):
        """
        Get the position of a Repellent
        :return: position of the agent as a tuple of coordinates
        """
        return self.pos
