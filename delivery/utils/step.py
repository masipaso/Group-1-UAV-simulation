class Step:
    """
    Simple class to store a position and the distance from that position to a target location
    Is used to store the route that a Uav has taken
    """
    def __init__(self, distance, pos):
        self.distance = distance
        self.pos = pos

