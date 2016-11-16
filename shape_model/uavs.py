from mesa import Agent
import random

class UAV(Agent):
    '''
    A UAV is an Agent that can move. It transports goods
    '''
    def __init__(self, model,pos,id):
        self.model = model
        self.pos = pos
        self.id= id
        pass

    def step(self):
        self.move()
        pass


    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = random.choice(possible_steps)
        while not self.model.grid.is_cell_empty(new_position):
            new_position = random.choice(possible_steps)
        old_position = self.pos
        self.model.grid.move_agent(self, new_position)
        print(' Agent: {}  Moves from {} to {}'.format(self.id, old_position,new_position))