class Item:
    """
    An Item is delivered by a drone.
    :param destination: A triple of coordinates representing the target destination to which the Item needs to be
                        delivered
    :param priority: A priority of the Item
    :param iid: A unique item identifier of the Item
    """
    def __init__(self, destination, priority=1, iid=0):
        self.pos = destination
        self.priority = priority
        self.iid = iid
        self.lifetime = 0
        self.pick_up_priority = 0
        self.delivered = False

    def step(self):
        """
        Override of step method. Will increase lifetime if item has not been delivered
        """
        if not self.delivered:
            self.lifetime += 1

    def set_delivered(self):
        """
        Mark an Item as delivered
        """
        self.delivered = True

    def get_destination(self):
        """
        Get the destination of the Item
        :return: destination of the Item as a tuple of coordinates
        """
        return self.pos

    def get_lifetime(self):
        """
        Get the lifetime of the Item
        :return: lifetime of item from creation
        """
        return self.lifetime
