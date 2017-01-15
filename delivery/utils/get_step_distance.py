def get_step_distance(pos1, pos2):
    """
    Calculate the step distance between two positions
    :param pos1: Tuple of coordinates
    :param pos2: Tuple of coordinates
    :return: The step-distance between both positions
    """
    if pos1 == pos2:
        return 0
    else:
        x = abs(pos1[0] - pos2[0])
        y = abs(pos1[1] - pos2[1])
        return max(x, y)
