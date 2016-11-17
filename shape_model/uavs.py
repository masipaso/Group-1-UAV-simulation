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
        pass

    def step(self):
        #self.move()
        self.moveMoreLogic()
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

    def moveMoreLogic(self):
        if self.pos == self.destination:
            return
        min_distance = 100.0
        neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius=10)
        possible_distance = []
        possible_steps = []
        myDistance = self.getEuclideanDistance(self.pos,self.destination)

        ''' Map possible fields to move to, to optimization of distance to destination
        What is absolutely missing: A step now might minimise the distance in the future?'''

        for element in neighborhood:
            if self.getEuclideanDistance(self.destination,element) == 0:
                min_distance = 0
                possible_distance.append((element, 0))
            elif self.getEuclideanDistance(self.destination,element) <= myDistance:
                min_distance=  self.getEuclideanDistance(self.destination,element)
                possible_distance.append((element,min_distance))

        if not possible_distance == []:
            for element in possible_distance:
                if element[1] == min_distance:
                    if self.model.grid.is_cell_empty(element[0]):
                        possible_steps.append(element[0])

        ''' If no distance optimizing neighboring field is found...'''

        if possible_steps == []:
            new_position = random.choice(neighborhood)
            while not self.model.grid.is_cell_empty(new_position):
                new_position = random.choice(neighborhood)
        else:
            new_position = random.choice(possible_steps)

        old_position = self.pos

        self.model.grid.move_agent(self, new_position)

        print(' Agent: {}  Moves from {} to {}'.format(self.id, old_position, new_position))
        print(' Agent: {}  Distance to Destination {}: {}'.format(self.id, self.destination,
                                                                  self.getEuclideanDistance(self.pos,
                                                                                            self.destination)))



    def setDestination(self, destination):
        self.destination = destination

    def getEuclideanDistance(self,pos1,pos2):
        ''' Calculate Euclidean distance '''
        if pos1 == pos2:
            return 0
        else:
            p0d0= math.pow(pos1[0]-pos2[0],2)
            p1d1= math.pow(pos1[1]-pos2[1],2)
            return math.sqrt(p0d0+p1d1)