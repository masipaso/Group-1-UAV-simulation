from collections import defaultdict

from mesa.visualization.ModularVisualization import VisualizationElement
from delivery.agents.BaseStation import BaseStation
from delivery.agents.uav.Uav import Uav


class RealWorldGrid(VisualizationElement):

    includes = ["RealWorldCanvas.js"]

    def __init__(self, grid_width, grid_height, canvas_width, canvas_height, background_image_source,
                 landscape_image_source):
        """
        Instantiate a new RealWorldGrid
        :param grid_width: Width of the grid (in cells)
        :param grid_height: Height of the grid (in cells)
        :param canvas_width: Width of the canvas to draw in the client, in pixels
        :param canvas_height: Height of the canvas to draw in the client, in pixels
        :param background_image_source: The source image for the obstacles
        :param landscape_image_source: The source image for additional elements (streets, ...)
        """
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.grid_width = grid_width
        self.grid_height = grid_height

        background_image_source += "_obstacles.png"

        new_element = ("new RealWorldCanvas({}, {}, {}, {}, '{}', '{}')".
                       format(self.canvas_width, self.canvas_height, self.grid_width, self.grid_height,
                              background_image_source, landscape_image_source))
        self.js_code = "elements.push(" + new_element + ");"

    def portrayal(self, agent):
        """
        Create the visualization of an agent
        :param agent: an agent in the model
        :return: a portrayal object
        """
        if agent is None:
            return

        x, y, z = agent.pos
        portrayal = {"x": x, "y": y, "w": 1, "h": 1}

        if type(agent) is BaseStation:
            portrayal["color"] = "#FFC319"
            portrayal["type"] = "BaseStation"
            portrayal["layer"] = 0
            portrayal["id"] = agent.bid
        elif type(agent) is Uav:
            portrayal["type"] = "Uav"
            portrayal["color"] = "rgb(0, 205, 255)"
            portrayal["layer"] = z
            portrayal["id"] = agent.uid
            if not agent.cargo_bay.is_empty():
                portrayal["item"] = agent.cargo_bay.get_destination()
        else:
            return

        return portrayal

    def render(self, model):
        """
        Get all agents that need to be drawn
        :param model: The model which needs to be visualized
        :return: A dictionary with different layers of agent portrayals
        """
        current_state = defaultdict(list)
        for agent in model.schedule.agents:
            portrayal = self.portrayal(agent)
            if portrayal:
                current_state[portrayal["layer"]].append(portrayal)
        return current_state