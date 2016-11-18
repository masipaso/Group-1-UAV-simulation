from mesa import Agent
import random
import math

class UAV(Agent):
    '''
    A UAV is an Agent that can move. It transports goods
    State: 1: empty, 2: carrying an item, 3: , 4: ....
    '''
    def __init__(self, model,pos,id,baseStations=[]):
        self.model = model
        self.pos = pos
        self.id= id
        self.destination = pos
        self.walk = []
        self.pastDistances = []
        self.item = None
        self.state = 1
        self.baseStations = baseStations
        pass

    def step(self):
        if self.state == 1:
            for base in self.baseStations:
                if base.pos == self.pos:
                    self.assignItem(base.pickupItem())
            pass

        elif self.state == 2:
            if self.pos == self.destination:
                self.item = None
                self.state = 1
            else:
                self.moveSimpleAlgorithm()
        pass

    def moveSimpleAlgorithm(self):

        if self.pos == self.destination:
            print(' Agent: {}  is at its Destination, {}'.format(self.id, self.destination))
            print(' Agent: {}  Needed {} steps and took this walk: {}'.format(self.id,len(self.walk)-1, self.walk))
            return

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

                possible_distance.clear()
                possible_distance.append((element, 0))
                break
            elif self.getEuclideanDistance(self.destination,element) <= myDistance:
                min_distance=  self.getEuclideanDistance(self.destination,element)
                possible_distance.append((element,min_distance))

        if not possible_distance == []:
            for element in possible_distance:
                if self.model.grid.is_cell_empty(element[0]):
                    possible_steps.append(element[0])

        ''' If no distance optimizing neighboring field is found...
            Repellent?

        '''
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
        print(' Agent: {}  Moves from {} to {}. Distance to Destination: {}'.format(self.id, old_position, new_position, new_distance))
        #print(' Agent: {}  Distance to Destination {}: {}'.format(self.id, self.destination,new_distance))

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

    def assignItem(self,item):

        if self.state==1 and item != None:
            self.item = item
            self.destination = item.getDestination()
            self.state = 2

    def deliver

    def getState(self):
        return self.state
