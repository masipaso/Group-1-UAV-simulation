import random

from shape_model.agents.repellent import Pheromones, Repellent
from shape_model.agents.baseStation import BaseStation


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
        #return neighborhood

        possible_distance = []
        possible_steps = []
        myDistance = self.uav.getEuclideanDistance(self.uav.pos, self.uav.destination)
        for element in neighborhood:
            if self.uav.getEuclideanDistance(self.uav.destination,element) == 0:

                possible_distance.clear()
                possible_distance.append((element, 0))
                break

            elif self.uav.getEuclideanDistance(self.uav.destination,element) <= myDistance:
                min_distance=  self.uav.getEuclideanDistance(self.uav.destination,element)
                possible_distance.append((element,min_distance))

        if not possible_distance == []:
            for element in possible_distance:
                if not self.uav.model.grid.is_cell_empty(element[0]):
                    cellcontents = self.uav.model.grid.get_cell_list_contents([(element[0])])
                    for obs in cellcontents:
                        if type(obs) is BaseStation or type(obs) is Pheromones:
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

        ''' Map possible fields to move to, to optimization of distance to destination
        What is absolutely missing: A step now might minimise the distance in the future?'''

        ''' If no distance optimizing neighboring field is found...
            Repellent?

        '''
        if possible_steps == []:
            new_position = random.choice(neighborhood)
            while not self.uav.model.grid.is_cell_empty(new_position):
                new_position = random.choice(neighborhood)
        else:
            new_position = random.choice(possible_steps)

        old_position = self.uav.pos

        self.uav.model.grid.move_agent(self.uav, new_position)

        new_distance = self.uav.getEuclideanDistance(self.uav.pos,self.uav.destination)
        print(' Agent: {}  Moves from {} to {}. Distance to Destination: {}'.format(self.uav.id, old_position, new_position, new_distance))
        #print(' Agent: {}  Distance to Destination {}: {}'.format(self.uav.id, self.uav.destination,new_distance))

        ''' Adding the new position to the walk'''
        self.uav.walk.append(new_position)
        pass


class AntAlgorithm(UAV_Algorithm):
    def run(self):
        neighborhood = self.uav.model.grid.get_neighborhood(
            self.uav.pos,
            moore=True,
            include_center=False,
            radius=1)
        possible_steps = self.getPossibleSteps()

        ''' Map possible fields to move to, to optimization of distance to destination
        What is absolutely missing: A step now might minimise the distance in the future?'''

        ''' If no distance optimizing neighboring field is found...
            Repellent?

        '''

        new_position = None
        lastposInWalk = self.uav.walk[-2:]

        if not possible_steps == []:
            for elem in possible_steps:
                if elem in lastposInWalk:
                    possible_steps.remove(elem)

        if not possible_steps == []:
            elem = possible_steps[0]
            if elem[1] == 0:
                new_position = elem[0]
                print(elem[0])
                possible_steps.clear()

        if not possible_steps == []:

            for elem in possible_steps:
                for cont in self.uav.model.grid.get_cell_list_contents(elem):
                    if type(cont) is Pheromones:
                        if self.uav.getEuclideanDistance(self.uav.destination,elem) < self.uav.getEuclideanDistance(self.uav.pos,self.uav.destination):
                            new_position= elem
                            cont.strengthen()
                        break

        if new_position == None:
            for elem in possible_steps:
                for cont in self.uav.model.grid.get_cell_list_contents(elem):
                    if type(cont) is Pheromones:
                        new_position= elem
                        cont.strengthen()
                        break

        if new_position == None:
            new_position = random.choice(self.getAllPossibleSteps())

        old_position = self.uav.pos

        self.uav.model.grid.move_agent(self.uav, new_position)

        new_distance = self.uav.getEuclideanDistance(self.uav.pos, self.uav.destination)
        print(' Agent: {}  Moves from {} to {}. Distance to Destination: {}'.format(self.uav.id, old_position,
                                                                                    new_position, new_distance))
        # print(' Agent: {}  Distance to Destination {}: {}'.format(self.uav.id, self.uav.destination,new_distance))

        ''' Adding the new position to the walk'''
        self.plant_pheromones(old_position)
        self.uav.walk.append(new_position)
        pass

    def plant_repellent(self,pos):
        repel = Repellent(model=self.uav.model, pos=pos)
        self.uav.model.grid.place_agent(repel, pos)


    def plant_pheromones(self,pos):
        print(' Agent: {}  planted a pheromone at {}'.format(self.uav.id,pos))
        phero = Pheromones(model=self.uav.model, pos=pos)
        self.uav.model.grid.place_agent(phero, pos)

    def getAllPossibleSteps(self):
        if self.uav.pos == self.uav.destination:
            print(' Agent: {}  is at its Destination, {}'.format(self.uav.id, self.uav.destination))
            print(' Agent: {}  Needed {} steps and took this walk: {}'.format(self.uav.id, len(self.uav.walk) - 1,
                                                                              self.uav.walk))
            return

        neighborhood = self.uav.model.grid.get_neighborhood(
            self.uav.pos,
            moore=True,
            include_center=False,
            radius=1)

        possible_distance = []
        possible_steps = []
        myDistance = self.uav.getEuclideanDistance(self.uav.pos, self.uav.destination)
        for element in neighborhood:
            if self.uav.getEuclideanDistance(self.uav.destination, element) == 0:
                possible_distance.clear()
                possible_distance.append((element, 0))
                break
            else:
                min_distance = self.uav.getEuclideanDistance(self.uav.destination, element)
                possible_distance.append((element, min_distance))

        #Remove already taken fields apart from the ones that contains base stations or pheromones
        if not possible_distance == []:
            for element in possible_distance:
                if not self.uav.model.grid.is_cell_empty(element[0]):
                    cellcontents = self.uav.model.grid.get_cell_list_contents([(element[0])])
                    for obs in cellcontents:
                        if type(obs) is BaseStation or type(obs) is Pheromones:
                            possible_steps.append(element[0])
                else:
                    possible_steps.append(element[0])

        return possible_steps
