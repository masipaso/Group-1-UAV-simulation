from mesa.time import RandomActivation
from collections import defaultdict
import random


class Schedule(RandomActivation):
    """
    A Scheduler which activates each type of agent once per step in random order.
    The random order is reshuffled in every step.
    """

    agents_by_type = defaultdict(list)

    def __init__(self, model):
        """
        Initialize the Schedule
        :param model: world model
        """
        super().__init__(model)
        self.agents_by_type = defaultdict(list)

    def add(self, agent):
        """
        Add an Agent object to the schedule
        :param agent: An Agent to be added to the schedule
        """
        self.agents.append(agent)
        agent_class = type(agent)
        self.agents_by_type[agent_class].append(agent)

    def remove(self, agent):
        """
        Remove all instances of a given agent from the schedule.
        """
        while agent in self.agents:
            self.agents.remove(agent)

        agent_class = type(agent)
        while agent in self.agents_by_type[agent_class]:
            self.agents_by_type[agent_class].remove(agent)

    def step(self, by_type=True):
        """
        Executes the step of each agent type in a random order (one by one)
        :param by_type: If True, run all agents of one type before running the next type
        """
        if by_type:
            for agent_class in self.agents_by_type:
                self.step_type(agent_class)
            self.steps += 1
            self.time += 1
        else:
            super.step()

    def step_type(self, type):
        """
        Shuffle the order and run all agents of one type
        :param type: Class object of the type to run
        """
        agents = self.agents_by_type[type]
        random.shuffle(agents)
        for agent in agents:
            agent.step()

    def get_type_count(self, agent_class):
        """
        Returns the number of agents of a certain type in the queue
        :param agent_class: Type of agents
        :return: Number of agents of type agent_class
        """
        return len(self.agents_by_type[agent_class])
