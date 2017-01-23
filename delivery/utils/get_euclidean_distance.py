import numpy


def get_euclidean_distance(pos1, pos2):
    """
    Calculate Euclidean distance (in a 3D environment)
    :param pos1: Triple of coordinates
    :param pos2: Triple of coordinates
    :return: The euclidean distance between both positions
    """
    return numpy.sqrt(numpy.square(abs(pos1[0]-pos2[0])) + numpy.square(abs(pos1[1]-pos2[1])) + numpy.square(abs(pos1[2]-pos2[2])))
