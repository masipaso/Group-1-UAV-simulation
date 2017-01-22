class Cell:
    def __init__(self, pos, altitude):
        self.pos = pos
        self.altitude = altitude
        self.parent = None
        # Calculated number of steps to get to this cell from the start
        self.g = 0
        # Guess remaining distance to the target
        self.h = 0
        # Combined estimated costs
        self.f = 0

    def update(self, g, h, parent):
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.parent = parent
