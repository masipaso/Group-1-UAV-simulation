class Item:
    """
    An Item is delivered by a drone.
    :param destination: A tuple of coordinates representing the target destination to which the Item needs to be
                        delivered
    :param priority: A priority of the Item
    :param iid: A unique item identifier of the Item
    """
    def __init__(self, destination, priority=1, iid=0):
        self.destination = destination
        self.priority = priority
        self.iid = iid
        self.lifetime = 0
        self.delivered = False

    def step(self):
        """
        Override of step method. Will increase lifetime if item has not been delivered
        """
        if not self.delivered:
            self.lifetime += 1

    def deliver(self, grid):
        """
        If an Item is delivered, remove it from the perceived_world_grid
        :param grid: The grid the Item was placed on (UAV perceived_grid)
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
        Get the lifetime of the Item
        :return: lifetime of item from creation
        """
        return self.lifetime
