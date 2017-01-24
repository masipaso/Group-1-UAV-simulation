import configparser

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from delivery.model.Worldmodel import WorldModel
from delivery.visualization.Perceived_world_grid import PerceivedWorldGrid
from delivery.visualization.Real_world_grid import RealWorldGrid

from delivery.visualization.VisualizationServer import VisualizationServer


def launch_world_model():

    # Read config file
    config = configparser.ConfigParser()
    config.read('./config.ini')
    # Get parameters
    width = config.getint('Grid', 'width')
    height = config.getint('Grid', 'height')
    pixel_ratio = config.getint('Grid', 'pixel_ratio')

    # Create Grids
    # real_world_grid - representing the 'actual' world
    real_world_grid = RealWorldGrid(width, height, width * pixel_ratio, height * pixel_ratio)

    # Create Chart
    chart = ChartModule([
        {"Label": "Items (Waiting)", "Color": "Red"},
        {"Label": "Items (Picked up)", "Color": "Orange"},
        {"Label": "Items (Delivered)", "Color": "Green"},
        {"Label": "UAVS", "Color": "#00BFFF"},
    ],
        data_collector_name='datacollector'
    )

    # Create Server
    server = VisualizationServer(WorldModel, [real_world_grid], "Delivery Simulation")
    server.port = 8521
    server.launch()