from collections import defaultdict

from mesa.visualization.modules import CanvasGrid

from delivery.agents.repellent import Repellent
from delivery.agents.baseStation import BaseStation
from delivery.agents.item import Item
from delivery.agents.uav.uav import Uav


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
        elif type(agent) is Uav:
            opacity = round(agent.current_charge / 100, 1)
            if opacity == 0:
                opacity = 0.1
            portrayal["Color"] = "rgba(0, 255, 255, " + str(opacity) + ")"

            if agent.state == 6:
                portrayal["Color"] = "rgb(255, 0, 255)"

            portrayal["text"] = agent.id
            portrayal["text_color"] = "#000000"
            portrayal["Shape"] = "rect"
            portrayal["Layer"] = 3
        elif type(agent) is Item:
            portrayal["Color"] = "#008000"
            portrayal["Shape"] = "rect"
            portrayal["Layer"] = 2
        elif type(agent) is Repellent:
            opacity = round(agent.strength / 100, 1)
            portrayal["Color"] = "rgba(255, 0, 0, " + str(opacity) + ")"
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
        self._remove_agent(agent.pos, agent)
        self._place_agent(pos, agent)
