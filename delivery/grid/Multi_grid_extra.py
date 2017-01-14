from mesa.space import MultiGrid
from delivery.agents.repellent import Repellent


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

    def get_repellent_on(self, pos):
        """
        Check if there is a repellent on the position
        :param pos: position that is checked
        :return: A repellent, that is on the position or None
        """
        cell_content = self.get_cell_list_contents(pos)
        for content in cell_content:
            if type(content) is Repellent:
                return content
        return None
