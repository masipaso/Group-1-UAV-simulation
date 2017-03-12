class CargoBay:
    """
    The CargoBay of an UAV
    """

    def __init__(self, item=None):
        """
        Initialize the CargoBay
        :param item: The item that is currently in the CargoBay
        """
        self.item = item

    def is_empty(self):
        """
        Check if the CargoBay is empty
        :return: True if there is no Item in the CargoBay, otherwise False
        """
        return True if self.item is None else False

    def store_item(self, item):
        """
        Stores an Item in the CargoBay
        :param item: The Item that is stored in the CargoBay
        """
        self.item = item

    def remove_item(self):
        """
        Removes an Item from the CargoBay
        """
        self.item.set_delivered()
        self.item = None

    def get_destination(self):
        """
        Get the destination of the Item
        :return: A tuple of coordinates if there is an Item, otherwise None
        """
        if self.item:
            return self.item.get_destination()
        return None

    def get_item(self):
        """
        Get the Item that is currently stored in the CargoBay
        :return: The Item
        """
        return self.item
