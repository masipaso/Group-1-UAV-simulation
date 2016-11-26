from mesa.visualization.modules import CanvasGrid

from shape_model.base_stations import BaseStation
from shape_model.obstacles import Obstacle
from shape_model.uavs import UAV


class RealWorldGrid(CanvasGrid):

    def __init__(self, grid_width, grid_height, canvas_width=500, canvas_height=500):
        """
        Instantiate a new CanvasGrid
        :param grid_width: Width of the grid (in cells)
        :param grid_height: Height of the grid (in cells)
        :param canvas_width: Width of the canvas to draw in the client, in pixels
        :param canvas_height: Height of the canvas to draw in the client, in pixels
        """
        super().__init__(self.world_portrayal, grid_width, grid_height, canvas_width, canvas_height)

    def world_portrayal(self, agent):
        """
        Create the visualization of an agent
        :param agent: an agent in the model
        :return: a portrayal object
        """
        if agent is None:
            return

        portrayal = {"Shape": "circle",
                     "Filled": "true"}

        if type(agent) is Obstacle:
            portrayal["Color"] = "rgba(0, 0, 0, 0.4)"
            portrayal["Shape"] = "rect"
            portrayal["Layer"] = 0
        elif type(agent) is BaseStation:
            portrayal["Color"] = "#FFC319"
            portrayal["Shape"] = "rect"
            portrayal["Layer"] = 1
        elif type(agent) is UAV:
            portrayal["Color"] = "#00BFFF"
            portrayal["Shape"] = "rect"
            portrayal["Layer"] = 2
        else:
            return

        portrayal["w"] = 1
        portrayal["h"] = 1

        return portrayal

    def move_agent(self, agent, pos):
        """
        Move an agent from its current position to a new position.

        Args:
            agent: Agent object to move. Assumed to have its current location
                   stored in a 'pos' tuple.
            pos: Tuple of new position to move the agent to.

        """
        print("my move function")
        self._remove_agent(agent.pos, agent)
        self._place_agent(pos, agent)