from mesa.visualization.ModularVisualization import VisualizationElement

from collections import defaultdict

from delivery.agents.baseStation import BaseStation
from delivery.agents.uav import Uav


class RealWorldGrid(VisualizationElement):

    local_includes = ["delivery/visualization/js/RealWorldCanvas.js"]

    def __init__(self, grid_width, grid_height, canvas_width=500, canvas_height=500):
        """
        Instantiate a new CanvasGrid
        :param grid_width: Width of the grid (in cells)
        :param grid_height: Height of the grid (in cells)
        :param canvas_width: Width of the canvas to draw in the client, in pixels
        :param canvas_height: Height of the canvas to draw in the client, in pixels
        """
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.grid_width = grid_width
        self.grid_height = grid_height

        new_element = ("new RealWorldCanvas({}, {}, {}, {})".
                       format(self.canvas_width, self.canvas_height, self.grid_width, self.grid_height))
        self.js_code = "elements.push(" + new_element + ");"

    def world_portrayal(self, agent):
        """
        Create the visualization of an agent
        :param agent: an agent in the model
        :return: a portrayal object
        """
        if agent is None:
            return

        portrayal = {"Filled": "true"}

        if type(agent) is BaseStation:
            portrayal["Color"] = "#FFC319"
            portrayal["Type"] = "BaseStation"
            portrayal["Layer"] = 1
        elif type(agent) is Uav:
            portrayal["Type"] = "Uav"
            portrayal["Color"] = "rgb(0, 205, 255)"
            portrayal["Layer"] = 2
        else:
            return

        portrayal["w"] = 1
        portrayal["h"] = 1

        return portrayal

    def render(self, model):
        grid_state = defaultdict(list)
        for x in range(model.grid.width):
            for y in range(model.grid.height):
                cell_objects = model.grid.get_cell_list_contents([(x, y)])
                for obj in cell_objects:
                    portrayal = self.world_portrayal(obj)
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
        self._remove_agent(agent.pos, agent)
        self._place_agent(pos, agent)