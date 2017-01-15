from delivery.agents.repellent import Repellent


class CommunicationModule:
    """
    The CommunicationModule of an UAV
    """
    # TODO: More details

    def __init__(self, perceived_world_grid, model):
        """
        Initialize the CommunicationModule
        :param perceived_world_grid: The UAV-specific grid for Repellents and Items
        :param model: The Model of the Simulation
        """
        self.perceived_world_grid = perceived_world_grid
        self.model = model

    def exchange_repellents_with(self, other_uav):
        # TODO: Avoid exchanging grids with a UAV that we just exchanged grids with!
        other_grid = self._receive_grid_from(other_uav)
        # Iterate over the grid of the other UAV ...
        for x in range(0, other_grid.width - 1):
            for y in range(0, other_grid.height - 1):
                # ... check if there is a Repellent on the position
                other_repellent = other_grid.get_repellent_on((x, y))
                my_repellent = self.perceived_world_grid.get_repellent_on((x, y))
                # If there is a Repellent on the position ...
                if other_repellent is not None:
                    # ... and there is a Repellent on my own grid
                    if my_repellent is not None:
                        # Check which Repellent was last updated ...
                        if my_repellent.get_last_updated_at() < other_repellent.get_last_updated_at():
                            # ... and update my own Repellent if the other one was updated more recently
                            my_repellent.set_strength(other_repellent.strength)
                            my_repellent.set_last_updated_at(self.model.steps)
                    # If I don't have a Repellent on that position:
                    else:
                        # ... place a new Repellent
                        new_repellent = Repellent(self.model, (x, y), self.perceived_world_grid)
                        new_repellent.set_strength(other_repellent.strength)
                        self.perceived_world_grid.place_agent(agent=new_repellent, pos=(x, y))

    @staticmethod
    def _receive_grid_from(other_uav):
        """
        Mock function which receives a grid from another UAV
        :param other_uav: The UAV which sends the perceived_world_grid
        :return: The perceived_world_grid from the other UAV
        """
        return other_uav.communication_module.send_grid()

    def send_grid(self):
        """
        Mock function which sends the perceived_world_grid of the UAV
        :return: The perceived_world_grid of the UAV
        """
        return self.perceived_world_grid


