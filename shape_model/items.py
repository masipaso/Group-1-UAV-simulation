
class Item():
    """
    An Item is delivered by a drone.
    """
    def __init__(self, destination, priority=1, id=0):
        self.destination = destination
        self.priority = priority
        self.id = id

    def getDestination(self):
        return self.destination

    def get_position(self):
        """
        Get the position of an Item
        :return: position of the agent as a tuple of coordinates
        """
        return self.destination
