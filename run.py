import configparser

from delivery.server import launch_world_model
from delivery.tests.tests_runner import tests_runner
from delivery.model.worldmodel import WorldModel


def run_gui():
    launch_world_model()

def run_no_gui(number_steps):
    print("\033[1mStart of Simulation without GUI\033[0m")
    model = WorldModel()
    for i in range(0,number_steps):
        print("Step {}".format(i))
        model.step()

    print("\033[1mSimulation terminated successfully\033[0m")

def run_tests():
    tests_runner().run_tests()

# Read config.cfg
config = configparser.ConfigParser()
config.read('./config.ini')
runmode = config.getint('Runmode', 'runmode')

if runmode == 1:
    run_gui()

elif runmode == 2:
    number_steps = config.getint('Runmode','number_steps')
    run_no_gui(number_steps=number_steps)

elif runmode == 3:
    run_tests()


else:
    print("Runmode setting in config.ini not correct!")
    print("1 = GUI, 2 = No GUI, 3 = Unittests")

# with open('trash', 'w'): pass
