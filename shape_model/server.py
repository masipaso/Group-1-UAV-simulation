import random

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from shape_model.obstacles import Obstacle
from shape_model.base_stations import BaseStation
from shape_model.uavs import UAV
from shape_model.items import Item

from shape_model.ants import Repellent, Pheromones
from shape_model.model import WorldModel


def world_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "Filled": "true"}

    if type(agent) is Obstacle:
        portrayal["Color"] = "rgba(0, 0, 0, 0.4)"
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is BaseStation:
        portrayal["Color"] = "#FFC319"
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is UAV:
        portrayal["Color"] = "#00bfff"
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 2
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Item:
        portrayal["Color"] = "#008000"
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Repellent:
        portrayal["Color"] = "#ff0000"
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Pheromones:
        portrayal["Color"] = "#008000"
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
    return portrayal

def launch_world_model():
    width = 101
    height = 101
    pixel_ratio = 8
    # Create Grid
    grid = CanvasGrid(world_portrayal, width, height, width * pixel_ratio, height * pixel_ratio)
    # Create Chart
    chart = ChartModule([
        {"Label": "Items (Waiting)", "Color": "Red"},
        {"Label": "Items (Picked up)", "Color": "Orange"},
        {"Label": "Items (Delivered)", "Color": "Green"},
        {"Label": "UAVS", "Color": "#00bfff"},
    ],
        data_collector_name='datacollector'
    )
    # Create Server
    worldmodel = WorldModel
    server = ModularServer(worldmodel, [grid, chart], "Delivery Simulation")
    server.port = 8521
    server.launch()


if __name__ == "__main__":
    random.seed(3)
    launch_world_model()