import configparser
from delivery.agents.Repellent import Repellent


class CommunicationModule:
    """
    The CommunicationModule of an UAV
    """
    # TODO: More details

    def __init__(self, perceived_world, model, max_altitude):
        """
        Initialize the CommunicationModule
        :param perceived_world: The UAV-specific grid for Repellents and Items
        :param model: The Model of the Simulation
        :param max_altitude: The maximum altitude
        """
        self.perceived_world = perceived_world
        self.model = model
        self.max_altitude = max_altitude

    def exchange_repellents_with(self, other_uav):
        other_perceived_world = self._receive_perceived_world_from(other_uav)
        # Iterate over all altitudes ...
        for altitude in range(1, self.max_altitude):
            # ... and check if there are Repellents stored on that altitude
            if other_perceived_world.has_repellents_on(altitude):
                # ... if there are at least on Repellent on the altitude
                # Check if I have Repellents on that altitude
                if self.perceived_world.has_repellents_on(altitude):
                    # ... if I do, we need to compare all Repellents
                    repellents = other_perceived_world.get_repellents_on(altitude)
                    for pos in repellents:
                        # Get the Repellent from the other perceived_world
                        other_repellent = other_perceived_world.get_repellent_on(pos, altitude)
                        # Check if there is a Repellent in my own perceived_world
                        my_repellent = self.perceived_world.get_repellent_on(pos, altitude)
                        if my_repellent is not None:
                            # I do have a Repellent on that position
                            # Compare which Repellent was last updated ...
                            if my_repellent.get_last_updated_at() < other_repellent.get_last_updated_at():
                                # ... and update my own Repellent if the other one was updated more recently
                                my_repellent.set_strength(other_repellent.strength)
                                my_repellent.set_last_updated_at(self.model.steps)
                        else:
                            # I don`t have a Repellent on that position
                            #  ... place a new one
                            new_repellent = Repellent(self.model, pos, self.perceived_world, altitude)
                            new_repellent.set_strength(other_repellent.strength)
                            self.perceived_world.place_repellent_at(new_repellent, pos, altitude)
                else:
                    # ... if I don´t, than I can just copy the other Repellents
                    self.perceived_world[altitude] = other_perceived_world.get_repellents_on(altitude).copy()

    @staticmethod
    def _receive_perceived_world_from(other_uav):
        """
        Mock function which receives a grid from another UAV
        :param other_uav: The UAV which sends the perceived_world
        :return: The perceived_world from the other UAV
        """
        return other_uav.communication_module.send_perceived_world()

    def send_perceived_world(self):
        """
        Mock function which sends the perceived_world_grid of the UAV
        :return: The perceived_world of the UAV
        """
        return self.perceived_world
