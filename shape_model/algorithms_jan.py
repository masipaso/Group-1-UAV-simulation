import random
from shape_model.base_stations import BaseStation
from shape_model.items import Item
from shape_model.ants import Repellent
from collections import defaultdict

from shape_model.Step import Step
from shape_model.obstacles import Obstacle


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

            available_steps = []
            possible_steps = []

            for cell in neighborhood:
                distance = self.uav.get_euclidean_distance(self.uav.destination, cell)
                available_step = Step(distance=distance, pos=cell)
                available_steps.append(available_step)

            available_steps.sort(key=lambda step: step.distance)
            for available_step in available_steps:
                # Remove all cell that contain an obstacle
                if not self.uav.model.grid.is_cell_empty(available_step.pos):
                    cell_contents = self.uav.model.grid.get_cell_list_contents([available_step.pos])
                    possible = True
                    for obstacle in cell_contents:
                        # If the obstacle is a not BaseStation, remove the cell as a possible step
                        if type(obstacle) is Obstacle or type(obstacle) is Repellent:
                            possible = False
                    if possible:
                        possible_steps.append(available_step)
                else:
                    possible_steps.append(available_step)


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
            y = abs(pos1[1] - pos2[1])
            return max(x, y)


    def run(self):
        possible_steps = self.get_possible_steps()
        #self.uav.last_repellent += 1

        last_position = self.uav.pos

        if possible_steps is []:
            print("no next steps")
        else:
            new_position = None
            for possible_step in possible_steps:
                print("new_position {}".format(possible_step))
                new_position = possible_step.pos
                if new_position is not 0:
                    break
            print("new_position {}".format(new_position))

            # Move UAV
            self.uav.model.grid.move_agent(self.uav, new_position)
            new_distance = self.uav.get_euclidean_distance(self.uav.pos, self.uav.destination)
            print(' Agent: {}  Moves from {} to {}. Distance to Destination: {}'.format(self.uav.id, last_position, new_position, new_distance))
            # Adding the new position to the walk
            self.uav.walk.append((new_position, new_distance))

            #print("walk {}".format(self.uav.walk))

            for index, step_taken in enumerate(reversed(self.uav.walk)):
                #print("last_repellent {}".format(self.uav.last_repellent))
                if index > self.uav.last_repellent:
                    break
                #print("step_taken {}, new_position {}".format(step_taken[0], new_position))
                # compare the expected distance to the actual distance
                # expected distance: amount of cells crossed to get to the current location
                expected_distance = self.get_step_distance(new_position, step_taken[0])
                # actual distance: number of walk entries from the current position to the step_taken
                actual_distance = index
                # if the expected_distance is smaller than the actual_distance a suboptimal route was found
                #print("expected {}, actual {}".format(expected_distance, actual_distance))
                if expected_distance < actual_distance:
                    print("Path was longer than expected!")
                    position = last_position
                    # if there is already a repellent on that position ...
                    if position in self.uav.model.repellents:
                        # ... increase its effect
                        print("is already a repellent on that pos")
                    else:
                        # ... or create a new one
                        self.uav.model.repellents.append(position)
                        repellent = Repellent(model=self.uav.model, pos=position)
                        self.uav.model.grid.place_agent(repellent, position)
                        self.uav.walk.remove(self.uav.walk[index])
                        #self.uav.last_repellent = 2
                    break
