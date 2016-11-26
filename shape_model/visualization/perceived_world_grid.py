from collections import defaultdict

from mesa.visualization.modules import CanvasGrid

from shape_model.agents.repellent import Repellent
from shape_model.agents.baseStation import BaseStation
from shape_model.agents.item import Item
from shape_model.agents.uav import UAV


class PerceivedWorldGrid(CanvasGrid):

    def __init__(self, grid_width, grid_height, canvas_width=500, canvas_height=500):
        """
        Instantiate a new CanvasGrid
        :param grid_width: Width of the grid (in cells)
        :param grid_height: Height of the grid (in cells)
        :param canvas_width: Width of the canvas to draw in the client, in pixels
        :param canvas_height: Height of the canvas to draw in the client, in pixels
        """
        super().__init__(self.perceived_portrayal, grid_width, grid_height, canvas_width, canvas_height)

    def perceived_portrayal(self, agent):
        """
        Create the visualization of an agent
        :param agent: an agent in the model
        :return: a portrayal object
        """
        if agent is None:
            return

        portrayal = {"Shape": "circle",
                     "Filled": "true"}

        if type(agent) is BaseStation:
            portrayal["Color"] = "#FFC319"
            portrayal["Shape"] = "rect"
            portrayal["Layer"] = 1
        elif type(agent) is UAV:
            portrayal["Color"] = "#00BFFF"
            portrayal["Shape"] = "rect"
            portrayal["Layer"] = 2
        elif type(agent) is Item:
            portrayal["Color"] = "#008000"
            portrayal["Shape"] = "rect"
            portrayal["Layer"] = 1
        elif type(agent) is Repellent:
            portrayal["Color"] = "#ff0000"
            portrayal["Shape"] = "rect"
            portrayal["Layer"] = 1
        else:
            return

        portrayal["w"] = 1
        portrayal["h"] = 1

        return portrayal

    def render(self, model):
        grid_state = defaultdict(list)
        for x in range(model.perceived_world_grid.width):
            for y in range(model.perceived_world_grid.height):
                cell_objects = model.perceived_world_grid.get_cell_list_contents([(x, y)])
                for obj in cell_objects:
                    portrayal = self.portrayal_method(obj)
                    if portrayal:
                        portrayal["x"] = x
                        portrayal["y"] = y
                        grid_state[portrayal["Layer"]].append(portrayal)

        return grid_state

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