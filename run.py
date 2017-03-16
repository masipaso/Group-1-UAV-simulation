import configparser

from delivery.Server import launch_world_model
from delivery.tests.tests_runner import TestRunner
from delivery.model.Worldmodel import WorldModel

def run_gui():
    """
    Run the simulation in GUI-mode
    :return:
    """
    launch_world_model()


def run_no_gui():
    """
    Run the simulation without a GUI
    :return:
    """
    print("\033[1mStart of Simulation without GUI\033[0m")
    model = WorldModel()
    for i in range(0, number_steps):
        model.step()

    print("\033[1mSimulation terminated successfully\033[0m")


def run_tests():
    """
    Run the test suite
    """
    TestRunner().run_tests()


# Read config.cfg
config = configparser.ConfigParser()
config.read('./config.ini')
run_mode = config.getint('Run_mode', 'run_mode')

if run_mode == 1:
    run_gui()

elif run_mode == 2:
    number_steps = config.getint('Run_mode', 'number_steps')
    run_no_gui()

elif run_mode == 3:
    run_tests()


else:
    print("Run mode setting in config.ini not correct!")
    print("1 = GUI, 2 = No GUI, 3 = Unittests")

