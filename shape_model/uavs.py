from mesa import Agent
import random
import math

class UAV(Agent):
    '''
    A UAV is an Agent that can move. It transports goods
    '''
    def __init__(self, model,pos,id):
        self.model = model
        self.pos = pos
        self.id= id
        self.destination = pos
        self.walk = []
        self.pastDistances = []
        pass

    def step(self):
        self.moveSimpleAlgorithm()
        pass


    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius=2)
        new_position = random.choice(possible_steps)
        while not self.model.grid.is_cell_empty(new_position):
            new_position = random.choice(possible_steps)
        old_position = self.pos

        self.model.grid.move_agent(self, new_position)

        print(' Agent: {}  Moves from {} to {}'.format(self.id, old_position,new_position))
        print(' Agent: {}  Distance to Destination {}: {}'.format(self.id, self.destination, self.getEuclideanDistance(self.pos,self.destination)))

    def moveSimpleAlgorithm(self):
        if self.pos == self.destination:
            print(' Agent: {}  is at its Destination, {}'.format(self.id, self.destination))
            print(' Agent: {}  Needed {} steps and took this walk: {}'.format(self.id,len(self.walk)-1, self.walk))
            return
        min_distance = 100.0
        neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius=1)
        possible_distance = []
        possible_steps = []
        myDistance = self.getEuclideanDistance(self.pos,self.destination)

        ''' Map possible fields to move to, to optimization of distance to destination
        What is absolutely missing: A step now might minimise the distance in the future?'''

        for element in neighborhood:
            if self.getEuclideanDistance(self.destination,element) == 0:
                min_distance = 0
                possible_distance.append((element, 0))
            elif self.getEuclideanDistance(self.destination,element) <= myDistance and self.getEuclideanDistance(self.destination,element)<= min_distance:
                min_distance=  self.getEuclideanDistance(self.destination,element)
                possible_distance.append((element,min_distance))

        if not possible_distance == []:
            for element in possible_distance:
                if element[1] == min_distance:
                    if self.model.grid.is_cell_empty(element[0]):
                        possible_steps.append(element[0])

        ''' If no distance optimizing neighboring field is found...'''
        ''' There is a lot to think of... We could optimize using the next bigger smaller distance to destination using neighbours of the last cell if we cannot optimize here and consider going back
        This also requires some kind of memory because in the next step it would just come back to this cell - Loop!'''
        if possible_steps == []:
            new_position = random.choice(neighborhood)
            while not self.model.grid.is_cell_empty(new_position):
                new_position = random.choice(neighborhood)
        else:
            new_position = random.choice(possible_steps)

        old_position = self.pos

        self.model.grid.move_agent(self, new_position)
        self.previousDistance = old_position
        new_distance = self.getEuclideanDistance(self.pos,self.destination)
        print(' Agent: {}  Moves from {} to {}'.format(self.id, old_position, new_position))
        print(' Agent: {}  Distance to Destination {}: {}'.format(self.id, self.destination,
                                                                  new_distance))

        ''' Adding the new position to the walk'''
        self.walk.append((new_position, new_distance))

    def setDestination(self, destination):
        self.destination = destination
        initialDistance = self.getEuclideanDistance(self.pos,self.destination)
        self.walk.append((self.pos,initialDistance))

    def getEuclideanDistance(self,pos1,pos2):
        ''' Calculate Euclidean distance '''
        if pos1 == pos2:
            return 0
        else:
            p0d0= math.pow(pos1[0]-pos2[0],2)
            p1d1= math.pow(pos1[1]-pos2[1],2)
            return math.sqrt(p0d0+p1d1)