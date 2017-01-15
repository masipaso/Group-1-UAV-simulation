from mesa.space import MultiGrid
from delivery.agents.Repellent import Repellent


class MultiGridExtra(MultiGrid):
    """
    A MultiGridExtra is a grid that extends MultiGrid's functionality
    """

    def __init__(self, width, height, torus):
        """
        Create a new MultiGridExtra
        :param width: width of the grid
        :param height: height of the grid
        :param torus: boolean whether the grid wraps or not
        """
        super().__init__(width, height, torus)

    def get_repellent_on(self, pos, altitude=1):
        """
        Check if there is a repellent on the position
        :param pos: Tuple of coordinates
        :param altitude: The altitude to check for
        :return: A repellent, that is on the position or None
        """
        cell_content = self.get_cell_list_contents(pos)
        for content in cell_content:
            if type(content) is Repellent:
                if content.altitude is altitude:
                    return content
        return None
