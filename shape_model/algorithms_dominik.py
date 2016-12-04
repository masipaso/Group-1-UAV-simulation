import random


from shape_model.agents.baseStation import BaseStation
from shape_model.agents.obstacle import Obstacle


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
                        if type(obs) is BaseStation:
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



class JumpPointAlgorithm():
    def __init__(self,uav):
        self.uav = uav
        self.weight = 2
        pass
    def run(self):
        # Get Neighborhood
        neighborhood = self.uav.model.grid.get_neighborhood(
            self.uav.pos,
            moore=True,
            include_center=False,
            radius=1)
        obstaclesNearby = []

        # Clean by Obstacles and add them to my obstaclelList
        neighborhood_list = []

        for neighbor in neighborhood:
            obstacleFound = 0
            cellcontents = self.uav.model.grid.get_cell_list_contents(neighbor)
            for obs in cellcontents:
                if type(obs) is Obstacle:
                    self.uav.obstacleList.append(neighbor)
                    obstacleFound = 1
                    break
            if not obstacleFound == 1:
                neighborhood_list.append((neighbor,self.uav.get_euclidean_distance(neighbor,self.uav.destination)))




        # Finde Obstacles in 5 Entfernung
            ## cut out obsts
        for elem in self.uav.obstacleList:
            if self.uav.get_euclidean_distance(elem,self.uav.pos) <= 2:
                obstaclesNearby.append(elem)

        # dist(elem,dest) > dist(elem,obst) and distance(uav,dest) > distance(elem,dest)
        if len(obstaclesNearby) >0: #Checke nach Obstacle-Kriterien
            index = 0
            for new_pos,new_distance_to_destination in neighborhood_list:
                for obst in obstaclesNearby:
                    if new_distance_to_destination > self.uav.get_euclidean_distance(new_pos,obst) and new_distance_to_destination < self.uav.get_euclidean_distance(self.uav.pos,self.uav.destination):
                        neighborhood_list[index] = (new_pos,new_distance_to_destination*self.weight)
                index += 1

        # Sort neighborhood list

        neighborhood_list = sorted(neighborhood_list, key=lambda distance: distance[1])
        last_position = self.uav.pos
        new_position = neighborhood_list.pop(0)[0]
        print('Trying to move to {}'.format(new_position))
        new_distance = self.uav.get_euclidean_distance(new_position,self.uav.destination)

        self.uav.move_to(new_position)
        new_distance = self.uav.get_euclidean_distance(self.uav.pos, self.uav.destination)
        print(' Agent: {}  Moves from {} to {}. Distance to Destination: {}'.format(self.uav.id, last_position,
                                                                                    new_position, new_distance))

        # Adding the new position to the walk
        self.uav.walk.append((new_position, new_distance))
        self.uav.realWalk.append((new_position, new_distance))




