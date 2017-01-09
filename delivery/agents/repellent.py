from mesa import Agent
import configparser


class Repellent(Agent):
    """
    A Repellent is an indicator that the cell in which the repellent is placed is not a good choice to move to
    """
    def __init__(self, model, pos, grid):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.grid = grid
        self.initialStrength = config.getfloat('Repellent','initialStrength')
        self.decreaseBy = config.getfloat('Repellent','decreaseBy')
        self.model = model
        self.pos = pos
        self.strength = self.initialStrength
        self.model.repellent_schedule.add(self)
        self.last_updated_at = self.model.steps


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
            #self.model.perceived_world_grid._remove_agent(self.pos, self)
            self.grid._remove_agent(self.pos,self)

            # ... and from the schedule
            self.model.repellent_schedule.remove(self)
        pass

    def weaken(self):
        """
        Weaken a Repellents strength
        """
        self.strength -= self.decreaseBy

    def strengthen(self):
        """
        Reset a Repellents strength
        """
        # TODO: Should we increase this by a number instead of setting it to a fixed value?
        self.last_updated_at = self.model.steps
        self.strength = self.initialStrength

    def get_position(self):
        """
        Get the position of a Repellent
        :return: position of the agent as a tuple of coordinates
        """
        return self.pos

    def get_last_updated_at(self):
        return self.last_updated_at

