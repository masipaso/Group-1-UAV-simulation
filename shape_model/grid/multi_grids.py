from mesa.space import MultiGrid

from shape_model.agents.repellent import Repellent


class TwoMultiGrid(MultiGrid):

    def __init__(self, width, height, torus):
        """
        Create a new TwoMultiGrid
        :param width: width of the grid
        :param height: height of the grid
        :param torus: boolean whether the grid wraps or not
        """
        super().__init__(width, height, torus)

    def move_agent(self, agent, pos):
        """
        Move an agent from its current position to a new position
        !! IMPORTANT: The position of the agent is not updated on the agent object itself !!
        :param agent: Agent object to move
        :param pos: Tuple of new position to move the agent to
        """
        self._remove_agent(agent.pos, agent)
        self._place_agent(pos, agent)

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
