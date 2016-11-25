import random
from shape_model.base_stations import BaseStation
from shape_model.items import Item
from shape_model.ants import Repellent
from collections import defaultdict


class UAV_Algorithm():
    '''
    An Item is delivered by a drone.
    '''
    def __init__(self,uav):
        self.uav = uav
        pass

    def run(self):
        pass

    def getPossibleSteps(self):
        if self.uav.pos == self.uav.destination:
            print(' Agent: {}  is at its Destination, {}'.format(self.uav.id, self.uav.destination))
            print(' Agent: {}  Needed {} steps and took this walk: {}'.format(self.uav.id,len(self.uav.walk)-1, self.uav.walk))
            return

        neighborhood = self.uav.model.grid.get_neighborhood(
            self.uav.pos,
            moore=True,
            include_center=False,
            radius=1)

        possible_distance = []
        possible_steps = []
        current_distance = self.uav.get_euclidean_distance(self.uav.pos, self.uav.destination)
        for element in neighborhood:
            if self.uav.get_euclidean_distance(self.uav.destination,element) == 0:
                possible_distance.clear()
                possible_distance.append((element, 0))
                break
            elif self.uav.get_euclidean_distance(self.uav.destination,element) <= current_distance:
                min_distance = self.uav.get_euclidean_distance(self.uav.destination,element)
                possible_distance.append((element, min_distance))

        if not possible_distance == []:
            for element in possible_distance:
                if not self.uav.model.grid.is_cell_empty(element[0]):
                    cell_contents = self.uav.model.grid.get_cell_list_contents([(element[0])])
                    for obstacle in cell_contents:
                        # If the obstacle is a BaseStation the drone can fly to its position
                        if type(obstacle) is BaseStation:
                            possible_steps.append(element[0])
                else:
                    possible_steps.append(element[0])

        return possible_steps


class SimpleAlgorithm(UAV_Algorithm):

    def run(self):
        neighborhood = self.uav.model.grid.get_neighborhood(
            self.uav.pos,
            moore=True,
            include_center=False,
            radius=1)
        possible_steps = self.getPossibleSteps()

        if possible_steps == []:
            new_position = random.choice(neighborhood)
            while not self.uav.model.grid.is_cell_empty(new_position):
                new_position = random.choice(neighborhood)
        else:
            new_position = random.choice(possible_steps)

        old_position = self.uav.pos

        self.uav.model.grid.move_agent(self.uav, new_position)

        new_distance = self.uav.get_euclidean_distance(self.uav.pos,self.uav.destination)
        print(' Agent: {}  Moves from {} to {}. Distance to Destination: {}'.format(self.uav.id, old_position, new_position, new_distance))

        ''' Adding the new position to the walk'''
        self.uav.walk.append(new_position)
        pass

class MyAlgorithm(UAV_Algorithm):

    def get_possible_steps(self):
        if self.uav.pos == self.uav.destination:
            print(' Agent: {}  is at its Destination, {}'.format(self.uav.id, self.uav.destination))
            print(' Agent: {}  Needed {} steps and took this walk: {}'.format(self.uav.id,len(self.uav.walk)-1, self.uav.walk))
            return []
        else:
            neighborhood = self.uav.model.grid.get_neighborhood(
                self.uav.pos,
                moore=True,
                include_center=False,
                radius=1)

            possible_steps = defaultdict(int)

            for cell in neighborhood:
                distance = self.uav.get_euclidean_distance(self.uav.destination, cell)
                possible_steps[distance] = cell

            for possible_step in sorted(possible_steps):
                # Remove all cell that contain an obstacle
                if not self.uav.model.grid.is_cell_empty(possible_steps[possible_step]):
                    cell_contents = self.uav.model.grid.get_cell_list_contents([possible_steps[possible_step]])
                    for obstacle in cell_contents:
                        # If the obstacle is a not BaseStation, remove the cell as a possible step
                        if type(obstacle) is not BaseStation and type(obstacle) is not Item:
                            if possible_steps[possible_step]:
                                del possible_steps[possible_step]

            return possible_steps

    def get_step_distance(self, pos1, pos2):
        '''
        Calculate the step distance between two positions
        :param pos1:
        :param pos2:
        :return:
        '''
        if pos1 == pos2:
            return 0
        else:
            x = abs(pos1[0] - pos2[0])
            y = abs(pos1[1] - pos1[1])
            return max(x, y)


    def run(self):
        # current position of the uav
        current_position = self.uav.pos
        # previous position of the uav
        last_position = self.uav.walk[len(self.uav.walk) - 2][0]
        print("current_position {}, last_position {}".format(current_position, last_position))
        possible_steps = self.get_possible_steps()

        if possible_steps is []:
            print("no next steps")
        else:
            print("walk {}".format(self.uav.walk))

            # compare the expected distance to the actual distance
            # expected distance: amount of cells crossed to get to the current location
            # actual distance: amount of steps taken (one step = one cell crossed) to get to the current location
            expected_distance = self.get_step_distance(current_position, last_position)
            print("expected_distance {}".format(expected_distance))
            actual_distance = self.get_step_distance()

            new_position = None
            for possible_step in sorted(possible_steps):
                new_position = possible_steps[possible_step]
                if new_position is not 0:
                    break
            print("new_position {}".format(new_position))

            self.uav.model.grid.move_agent(self.uav, new_position)
            new_distance = self.uav.get_euclidean_distance(self.uav.pos, self.uav.destination)
            print(' Agent: {}  Moves from {} to {}. Distance to Destination: {}'.format(self.uav.id, current_position, new_position, new_distance))
            # Adding the new position to the walk
            self.uav.walk.append((new_position, new_distance))