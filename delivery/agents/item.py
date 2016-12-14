
class Item:
    """
    An Item is delivered by a drone.
    """
    def __init__(self, destination, priority=1, id=0):
        self.destination = destination
        self.priority = priority
        self.id = id

    def deliver(self, grid):
        """
        If an Item is delivered, remove it from the perceived_world_grid
        :param grid:
        :return:
        """
        grid._remove_agent(self.destination, self)  # disregard the _

    def get_destination(self):
        """
        Get the destination of the Item
        :return: destination of the Item as a tuple of coordinates
        """
        return self.destination
