import configparser

from mesa.visualization.modules import ChartModule

from delivery.model.WorldModel import WorldModel
from delivery.visualization.RealWorldGrid import RealWorldGrid
from delivery.visualization.Details import Details

from delivery.visualization.VisualizationServer import VisualizationServer


def launch_world_model():
    # Read config file
    config = configparser.ConfigParser()
    config.read('./config.ini')
    # Get parameters
    width = config.getint('Grid', 'width', fallback=500)
    height = config.getint('Grid', 'height', fallback=500)
    pixel_ratio = config.getint('Grid', 'pixel_ratio', fallback=10)

    # real_world_grid - representing the 'actual' world
    real_world_grid = RealWorldGrid(width, height, width * pixel_ratio, height * pixel_ratio)

    # Detail information
    details = Details()

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
    server = VisualizationServer(WorldModel, [real_world_grid, details], "Delivery Simulation")
    server.port = 8521
    server.launch()
