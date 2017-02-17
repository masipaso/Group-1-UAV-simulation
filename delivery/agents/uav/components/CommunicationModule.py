class CommunicationModule:
    """
    The CommunicationModule of an UAV
    """

    def __init__(self, perceived_world, max_altitude):
        """
        Initialize the CommunicationModule
        :param perceived_world: The UAV-specific grid for Repellents and Items
        :param max_altitude: The maximum altitude
        """
        self.perceived_world = perceived_world
        self.max_altitude = max_altitude

    def exchange_grid_with(self, other_uav):
        """
        Exchange the perceived world between two UAVs.
        :param other_uav: The UAV to exchange the knowledge with
        """
        other_perceived_world = self._receive_perceived_world_from(other_uav)
        for altitude in range(0, self.max_altitude):
            self.perceived_world.perceived_world[altitude] = {**self.perceived_world.perceived_world[altitude], **other_perceived_world.perceived_world[altitude]}

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
