
class Item():
    '''
    An Item is delivered by a drone.
    '''
    def __init__(self, destination, priority=1,id=0):
        self.destination = destination
        self.priority = priority
        self.id = id

    def getDestination(self):
        return self.destination




