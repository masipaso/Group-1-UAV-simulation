import configparser
import sys

from mesa.visualization.modules import ChartModule

from delivery.model.Worldmodel import WorldModel
from delivery.visualization.RealWorldGrid import RealWorldGrid
from delivery.visualization.Details import Details

from delivery.visualization.VisualizationServer import VisualizationServer


def launch_world_model():
    # Read config file
    config = configparser.ConfigParser()
    config.read('./config.ini')
    # Get parameters
    try:
        width = config.getint('Grid', 'width', fallback=500)
    except ValueError:
        print("[Configuration] The width is not valid.")
        sys.exit(1)

    try:
        height = config.getint('Grid', 'height', fallback=500)
    except ValueError:
        print("[Configuration] The height is not valid.")
        sys.exit(1)

    try:
        pixel_ratio = config.getint('Grid', 'pixel_ratio', fallback=10)
    except ValueError:
        print("[Configuration] The pixel_ratio is not valid.")
        sys.exit(1)

    background_image_source = config.get('Grid', 'image',
                                         fallback='./delivery/visualization/images/a_city500x500.jpg')
    if type(background_image_source) is not str:
        print("[Configuration] The image is not valid.")
        sys.exit(1)

    try:
        background_image_source = background_image_source.split("/").pop()
        background_image_source = background_image_source.split(".")
        if background_image_source[len(background_image_source) - 1] != "jpg":
            raise ValueError
    except Exception:
        print("[Configuration] The image is not valid.")
        sys.exit(1)

    landscape_image_source = config.get('Grid', 'landscape_image',
                                        fallback='./delivery/visualization/images/a_city500x500_background.jpg')
    if type(landscape_image_source) is not str:
        print("[Configuration] The landscape_image is not valid.")
        sys.exit(1)

    try:
        landscape_image_source = landscape_image_source.split("/").pop()
        landscape_image_source = landscape_image_source.split(".")
        if landscape_image_source[len(landscape_image_source) - 1] != "jpg":
            raise ValueError
    except Exception:
        print("[Configuration] The landscape_image is not valid.")
        sys.exit(1)

    # real_world_grid - representing the 'actual' world
    real_world_grid = RealWorldGrid(width, height, width * pixel_ratio, height * pixel_ratio, background_image_source[0],
                                    landscape_image_source[0] + ".jpg")

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
