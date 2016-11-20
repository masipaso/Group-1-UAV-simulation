from mesa import Agent
import random
import math
from shape_model.base_stations import BaseStation

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
                    return
            if self.item == None:
                self.moveSimpleAlgorithm()
                return

        elif self.state == 2 and self.getEuclideanDistance(self.pos,self.destination)==0:
            self.deliver()
            return

        elif self.state == 2:
            self.moveSimpleAlgorithm()


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

        nextStepIsDest = 0
        for element in neighborhood:
            if self.getEuclideanDistance(self.destination,element) == 0:

                possible_distance.clear()
                possible_distance.append((element, 0))


            elif self.getEuclideanDistance(self.destination,element) <= myDistance:
                min_distance=  self.getEuclideanDistance(self.destination,element)
                possible_distance.append((element,min_distance))

        if not possible_distance == []:
            for element in possible_distance:
                if not self.model.grid.is_cell_empty(element[0]):
                    cellcontents = self.model.grid.get_cell_list_contents([(element[0])])
                    for obs in cellcontents:
                        if type(obs) is BaseStation:
                            possible_steps.append(element[0])
                else:
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
            self.destination = self.item.getDestination()
            print(' Agent: {}  Received Item {}. Delivering to {}. Distance to Destination: {}'.format(self.id, item.id,self.destination, self.getEuclideanDistance(self.pos,self.destination)))
            self.state = 2

    def deliver(self):
        flytobase = random.choice(self.baseStations)
        self.destination = flytobase.pos
        print(' Agent: {}  Delivered Item {} to {}. Flying back to base at: {}'.format(self.id, self.item.id,self.pos,self.destination))
        self.item = None
        self.state = 1
        # Notify model that a delivery was made
        self.model.number_of_delivered_items =+ 1

    def getState(self):
        return self.state
