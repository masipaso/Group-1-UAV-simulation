from mesa.space import MultiGrid

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