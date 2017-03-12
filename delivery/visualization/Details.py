from mesa.visualization.ModularVisualization import VisualizationElement
from delivery.agents.BaseStation import BaseStation
from delivery.agents.uav.Uav import Uav
from delivery.agents.Item import Item


class Details(VisualizationElement):

    includes = ["Details.js"]

    def __init__(self):
        """
        Instantiate a new Details component
        """

        self.js_code = "elements.push(new Details());"

    def portrayal(self, agent, step):
        """
        Create the visualization of an agent
        :param agent: an agent in the model
        :return: a portrayal object
        """
        if agent is None:
            return

        x, y, z = agent.pos
        portrayal = {"x": x, "y": y, "z": z, "step": step}

        if type(agent) is BaseStation:
            portrayal["type"] = "BaseStation"
            portrayal["id"] = agent.bid
            portrayal["picked_up_item"] = agent.get_number_of_items(True)
            portrayal["total_items"] = agent.item_counter
            portrayal["waiting_items"] = agent.get_number_of_items(False)
            portrayal["max_items"] = agent.max_items_per_base_station
            portrayal["waiting_items_by_priority"] = agent.get_number_of_items(False, True)
        elif type(agent) is Uav:
            portrayal["type"] = "UAV"
            portrayal["id"] = agent.uid
            portrayal["destination"] = agent.destination
            portrayal["battery_charge"] = agent.battery.get_charge()
            portrayal["battery_low"] = agent.battery.is_low()
            portrayal["battery_empty"] = agent.battery.is_empty()
            portrayal["battery_max"] = agent.battery.get_max_charge()
            if not agent.cargo_bay.is_empty():
                portrayal["item"] = agent.cargo_bay.get_destination()
        if type(agent) is Item:
            portrayal["type"] = "Item"
            portrayal["id"] = agent.iid
            portrayal["priority"] = agent.priority
            portrayal["lifetime"] = agent.get_lifetime()

        return portrayal

    def render(self, model):
        """
        Get all the requested detail information
        :param model: The model which needs to be visualized
        :return: A dictionary with different details to display
        """
        if model.details_for is not None:
            return self.portrayal(model.details_for, model.steps)
        return {"step": model.steps}