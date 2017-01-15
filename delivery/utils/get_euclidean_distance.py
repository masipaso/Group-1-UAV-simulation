import math


def get_euclidean_distance(pos1, pos2):
    """
    Calculate Euclidean distance
    :param pos1: Tuple of coordinates
    :param pos2: Tuple of coordinates
    :return: The euclidean distance between both positions
    """
    if pos1 == pos2:
        return 0
    else:
        p0d0 = math.pow(pos1[0] - pos2[0], 2)
        p1d1 = math.pow(pos1[1] - pos2[1], 2)
        return math.sqrt(p0d0 + p1d1)
