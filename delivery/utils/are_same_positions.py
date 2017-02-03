def are_same_positions(pos1, pos2):
    """
    Compare two positions
    :param pos1: Triple of coordinates
    :param pos2: Triple of coordinates
    :return: True, if both positions are the same. Otherwise, false.
    """
    if pos1 is None or pos2 is None:
        return False
    if pos1[0] == pos2[0] and pos1[1] == pos2[1] and pos1[2] == pos2[2]:
        return True
    return False