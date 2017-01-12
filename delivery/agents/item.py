class Item:
    """
    An Item is delivered by a drone.
    """
    def __init__(self, destination, priority=1, id=0):
        self.destination = destination
        self.priority = priority
        self.id = id
        self.lifetime = 0
        self.delivered = False

    def step(self):
        """
        Override of step method. Will increase lifetime if item has not been delivered
        :return:
        """
        if not self.delivered:
            self.lifetime += 1

    def deliver(self, grid):
        """
        If an Item is delivered, remove it from the perceived_world_grid
        :param grid:
        :return:
        """
        self.delivered = True
        grid._remove_agent(self.destination, self)  # disregard the _

    def get_destination(self):
        """
        Get the destination of the Item
        :return: destination of the Item as a tuple of coordinates
        """
        return self.destination

    def get_lifetime(self):
        """
        :return: lifetime of item from creation
        """
        return self.lifetime
