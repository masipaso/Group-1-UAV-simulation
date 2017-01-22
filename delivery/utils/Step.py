class Step:
    """
    Simple class to store a position and the distance from that position to a target location
    Is used to store the route that a Uav has taken
    """
    def __init__(self, distance, pos, altitude):
        """
        Initialize a Step
        :param distance: Distance between a destination point and the pos of the Step
        :param pos: Tuple of coordinates
        :param altitude: The altitude of the Step
        """
        self.distance = distance
        self.pos = pos
        self.altitude = altitude
