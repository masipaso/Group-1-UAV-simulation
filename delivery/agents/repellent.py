from mesa import Agent
import configparser


class Repellent(Agent):
    """
    A Repellent is an indicator that the cell in which the repellent is placed is not a good choice to move to
    """
    def __init__(self, model, pos, grid, altitude):
        """
        Initialize the Repellent
        :param model: world model
        :param pos: Tuple of coordinates at which the Repellent is located
        :param grid: The grid on which the Repellent is placed
        :param altitude: The altitude in which the Repellent is placed
        """
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.grid = grid
        self.initial_strength = config.getfloat('Repellent', 'initial_strength')
        self.decrease_by = config.getfloat('Repellent', 'decrease_by')
        self.model = model
        self.pos = pos
        self.strength = self.initial_strength
        self.model.repellent_schedule.add(self)
        self.last_updated_at = self.model.steps
        self.altitude = altitude
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
            self.grid._remove_agent(self.pos,self)
            # ... and from the schedule
            self.model.repellent_schedule.remove(self)
        pass

    def weaken(self):
        """
        Weaken a Repellents strength
        """
        self.strength -= self.decrease_by

    def strengthen(self):
        """
        Reset a Repellents strength
        """
        self.last_updated_at = self.model.steps
        # TODO: Should we increase this by a number instead of setting it to a fixed value?
        self.strength = self.initial_strength

    def get_position(self):
        """
        Get the position of a Repellent
        :return: Position of the agent as a tuple of coordinates
        """
        return self.pos

    def get_last_updated_at(self):
        """
        Get the step at which the Repellent was last updated
        :return: The step at which the Repellent was last updated
        """
        return self.last_updated_at

    def set_last_updated_at(self, step):
        """
        Set the step the Repellent was last seen at
        :param step: The step at which the Repellent was last seen
        """
        self.last_updated_at = step

    def set_strength(self, strength):
        """
        Set the strength of the Repellent
        :param strength: The new strength
        """
        self.strength = strength
