from mesa import Agent
# Import components
from delivery.grid.PerceivedWorldGrid import PerceivedWorldGrid
from delivery.agents.uav.components.FlightController import FlightController
from delivery.agents.uav.components.Battery import Battery
from delivery.agents.uav.components.CargoBay import CargoBay
from delivery.agents.uav.components.CommunicationModule import CommunicationModule
from delivery.agents.uav.components.Sensor import Sensor
# Import Utilis
from delivery.utils.get_euclidean_distance import get_euclidean_distance


class Uav(Agent):
    """
    A Uav is an Agent that can move. It transports Item from BaseStations to their destination
    State:
        1: idle at BaseStation,
        2: carrying an Item
        3: on the way to a Base Station
        4: battery low
        5: charging
        6: stranded without battery life left
    """
    def __init__(self, model, pos, uid, max_charge, battery_low, battery_decrease_per_step, battery_increase_per_step,
                 base_station, max_altitude, sensor_range):
        """
        Initialize the UAV
        :param model: world model
        :param pos: Tuple of coordinates at which the UAV is located
        :param uid: Unique UAV identifier
        :param max_charge: The maximum charge the battery can have
        :param battery_low: The threshold at which the battery charge is considered low
        :param battery_decrease_per_step: The decrease in battery charge per step
        :param battery_increase_per_step: The increase in battery charge while charging per step
        :param base_station: The 'home' BaseStation
        :param max_altitude: The max altitude that is allowed
        :param sensor_range: The range the the Sensor can cover
        """
        self.pos = pos
        self.uid = uid
        self.destination = None
        self.walk = []
        self.state = 1
        self.max_altitude = max_altitude

        # Construct UAV
        # Create a UAV-specific grid for Repellents and Item destinations
        self.perceived_world = PerceivedWorldGrid(max_altitude)
        # Add FlightController
        self.flight_controller = FlightController(self)
        self.last_repellent = 2
        # Add Battery
        self.battery = Battery(max_charge, battery_low, battery_decrease_per_step, battery_increase_per_step)
        # Add CargoBay
        self.cargo_bay = CargoBay(item=None)
        # Add CommunicationModule
        self.communication_module = CommunicationModule(self.perceived_world, max_altitude)
        # Add Sensor
        self.sensor = Sensor(model.schedule.agents_by_type[Uav], model.landscape, self.perceived_world, sensor_range)

        # Base Stations
        self.base_station = base_station
        # Delivery
        self.initial_delivery_distance = 0
        # This is the ratio of direct walk (initial distance, euclidean) against Length of actual walk taken.
        # This value is calculated on every delivery for every order.
        self.walk_length_divided_by_initial_distance = []
        self.real_walk = []
        # On arrival at a destination, the UAV will store how many steps it took to deliver an item
        self.walk_lengths = []

        super().__init__(uid, model)

    def step(self):
        """
        Advance the Uav one step
        """
        # If the UAV is IDLE at a BaseStation

        if self.state == 1:
            if self.base_station.get_pos() == self.pos:
                # ... try to pick up an Item if one is available
                self.pick_up_item(self.base_station.get_item())
                return
            # ... otherwise wait for an Item
        # If the UAV is carrying an Item
        elif self.state == 2:
            # ... and has reached the destination
            if self.pos == self.destination:
                self.deliver_item()
            # ... otherwise keep delivering the Item
            self.find_uavs_close()
            self.flight_controller.make_step()
        # If the UAV is on the way to a BaseStation
        elif self.state == 3:
            # ... and has reached the BaseStations
            if self.pos == self.destination:
                # ... update the state
                self.arrive_at_base_station(idle=True, charge=True)
            # .. otherwise keep finding the BaseStation
            else:
                self.find_uavs_close()
                self.flight_controller.make_step()
        # If the UAV is low on battery life
        elif self.state == 4:
            # ... and has reached the BaseStations
            if self.pos == self.destination:
                # ... update the state
                self.arrive_at_base_station(charge=True)
            # .. otherwise keep finding the BaseStation
            else:
                self.find_uavs_close()
                self.flight_controller.make_step()
        # If the UAV is charging the battery at a BaseStation
        elif self.state == 5 or self.state == 1:
            # ... charge the battery
            self.battery.charge()
            # print(' Agent: {}  charges battery. Battery: {}'.format(self.uid, self.battery.get_charge()))
        # If the UAV has no battery life left
        elif self.state == 6:
            # ... do nothing ... RIP
            return

        # Decrease battery life
        if self.state == 2 or self.state == 3 or self.state == 4:
            self.battery.discharge()

        # ... and check the status of the battery
        self.check_battery()

        return

    def check_battery(self):
        """
        Check if the current charge of the battery is sufficient to carry on, otherwise
        the UAV heads towards the closest Base Station for charging
        """
        # If the UAV is charging ...
        if self.state is 5:
            # ... and the battery is fully charged
            if self.battery.is_charged():
                # ... set the state to the previous state
                # If the UAV doesn't carry an Item
                if self.cargo_bay.is_empty():
                    # ... keep idleing
                    self.state = 1
                # Otherwise resume the delivery
                else:
                    self.state = 2
                    self.destination = self.cargo_bay.get_destination()
        # If the Battery is low ...
        elif self.battery.is_low():
            # .. adjust the state
            self.state = 4
            # ... and head to the next BaseStation to charge
            self.destination = self.flight_controller.get_nearest_base_station()
        # If the Battery is empty ...
        elif self.battery.is_empty():
            # ... adjust the state
            self.state = 6

    def pick_up_item(self, item):
        """
        The Uav picks up an Item at a BaseStation if the Uav is on the way to the BaseStation
        :param item: the Item that is picked up
        """
        # If there is an Item ...
        if item is not None:
            # ... store it in the CargoBay
            self.cargo_bay.store_item(item)
            # .. set the destination
            self.destination = self.cargo_bay.get_destination()
            # .. adjust the state
            self.state = 2
            # Clear out the previous walk
            self.walk = []
            self.real_walk = []
            self.initial_delivery_distance = get_euclidean_distance(self.pos, self.destination)

    def deliver_item(self):
        """
        The Uav delivers an Item
        """
        # Store iid for logging
        item = self.cargo_bay.get_item()
        iid = item.iid
        # ... remove the Item from the CargoBay
        self.model.item_schedule.remove(item)
        self.cargo_bay.remove_item()
        # ... adjust the state
        self.state = 3
        # ... notify model that a delivery was made
        self.model.number_of_delivered_items += 1

        # ... fly back to the base station
        self.destination = self.base_station.get_pos()

        # Clear out the previous walk
        self.walk = []
        self.walk_lengths.append(len(self.real_walk))
        self.walk_length_divided_by_initial_distance.append(len(self.real_walk) / self.initial_delivery_distance)
        self.initial_delivery_distance = None
        self.real_walk = []

    def arrive_at_base_station(self, idle=False, charge=False):
        """
        The UAV arrives at the Base Station
        :param idle: Indicator if the UAV should be IDLE in the next step
        :param charge: Indicator if the UAV should be charging in the next step
        :return:
        """
        # Update state
        if charge:
            self.state = 5
        if idle:
            self.state = 1

    def get_walk_lengths(self):
        """
        Get the lengths of the walk
        :return: Length of the walk
        """
        return self.walk_lengths

    def get_walk_length_divided_by_initial_distance(self):
        """
        Return KPI "Initial Delivery Distance by Avg. Walk length". This is the ratio of direct walk (euclidean) against
        Length of actual walk taken. This value is calculated on every delivery for every order.
        """
        return self.walk_length_divided_by_initial_distance

    def find_uavs_close(self):
        """
        Locate UAVs that are close and exchange grids
        """

        # Avoid immediate exchange
        if self.model.steps <= 20:
            return

        # Scan for UAVs
        other_uavs = self.sensor.scan_for_uavs(self.pos)
        # If there are other UAVs ...
        if len(other_uavs) is not 0:
            # ... exchange perceived_world_grids with them
            for other_uav in other_uavs:
                self.communication_module.exchange_grid_with(other_uav)
