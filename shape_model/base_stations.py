from mesa import Agent


class BaseStation(Agent):
    '''
    A BaseStation is an Agent that cannot move
    '''
    def __init__(self, model,pos):
        pass

    def step(self):
        pass

