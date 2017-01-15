from mesa import Agent
# Import components
from delivery.grid.Multi_grid_extra import MultiGridExtra
from delivery.agents.uav.components.FlightController import FlightController
from delivery.agents.uav.components.Battery import Battery
from delivery.agents.uav.components.CargoBay import CargoBay
from delivery.agents.uav.components.CommunicationModule import CommunicationModule
from delivery.agents.uav.components.Radar import Radar
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
                 base_station, altitude):
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
        :param altitude: The height the UAV is flying in
        """
        # TODO: Why do we have the model here? This should not be available
        self.model = model
        self.pos = pos
        self.uid = uid
        self.destination = None
        self.walk = []
        self.state = 1
        self.altitude = altitude

        # Construct UAV
        # Create a UAV-specific grid for Repellents and Item destinations
        self.perceived_world_grid = MultiGridExtra(height=self.model.grid.height, width=self.model.grid.width,
                                             torus=self.model.grid.torus)
        # Add FlightController
        self.flight_controller = FlightController(self)
        self.last_repellent = 2
        # Add Battery
        self.battery = Battery(max_charge, battery_low, battery_decrease_per_step, battery_increase_per_step)
        # Add CargoBay
        self.cargo_bay = CargoBay(item=None)
        # Add CommunicationModule
        self.communication_module = CommunicationModule(self.perceived_world_grid, model)
        # Add Radar
        # TODO: Make the coverage_range configurable
        # TODO: When we make this configurable, we have to adjust the FlighController!
        self.radar = Radar(model.grid, model.landscape, coverage_range=1)

        # Base Stations
        self.base_station = base_station
        # Delivery
        self.initial_delivery_distance = 0
        self.initial_delivery_distance_divided_by_average_walk_length = []
        # ??
        self.real_walk = []
        self.walk_lengths = []
        self.obstacle_list = []
        pass

    def step(self):
        """
        Advance the Uav one step
        """
        # If the UAV is IDLE at a BaseStation

        if self.state == 1:
            if self.base_station.pos == self.pos:
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
            print(' Agent: {}  charges battery. Battery: {}'.format(self.uid, self.battery.get_charge()))
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
                print(' Agent: {} is fully charged'.format(self.uid))
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
            print(' Agent: {}  has low Battery. going to Base Station: {}'.format(self.uid, self.destination))
        # If the Battery is empty ...
        elif self.battery.is_empty():
            # ... adjust the state
            self.state = 6
            print(' Agent: {}  has no Battery life left.'.format(self.uid))

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
            # TODO: Optional
            # ... place the Item on the perceived grid of the UAV
            self.perceived_world_grid.place_agent(pos=item.destination, agent=item)
            # .. adjust the state
            self.state = 2
            # Clear out the previous walk
            self.walk = []
            self.initial_delivery_distance = get_euclidean_distance(self.pos, self.destination)
            print(' Agent: {} Received Item {}. Delivering to {}. Distance to Destination: {}. Battery: {}'
                  .format(self.uid, item.iid, self.destination, get_euclidean_distance(self.pos, self.destination),
                          self.battery.get_charge()))

    def deliver_item(self):
        """
        The Uav delivers an Item
        """
        # Store iid for logging
        iid = self.cargo_bay.get_item().iid
        # ... remove the Item from the perceived grid of the UAV
        self.perceived_world_grid._remove_agent(self.cargo_bay.get_destination(), self.cargo_bay.get_item())
        # ... remove the Item from the CargoBay
        self.cargo_bay.remove_item()
        # ... adjust the state
        self.state = 3
        # ... notify model that a delivery was made
        # TODO: Make this more beautiful!
        self.model.number_of_delivered_items += 1
        # ... pick a BaseStation
        self.destination = self.flight_controller.choose_base_station_to_pick_up_item_from()

        # Clear out the previous walk
        self.walk = []
        self.walk_lengths.append(len(self.real_walk))
        self.initial_delivery_distance_divided_by_average_walk_length.append(len(self.real_walk)
                                                                             / self.initial_delivery_distance)
        self.initial_delivery_distance = []
        self.real_walk = []

        print(' Agent: {}  Delivered Item {} to {}. Flying back to base at: {}. Battery: {}'
              .format(self.uid, iid, self.pos, self.destination, self.battery.get_charge()))
        print(' Agent: {}  Needed {} steps and took this walk: {}'
              .format(self.uid, len(self.walk) - 1, self.walk))

    def arrive_at_base_station(self, idle=False, charge=False):
        """
        The UAV arrives at the Base Station
        :param idle: Indicator if the UAV should be IDLE in the next step
        :param charge: Indicator if the UAV should be charging in the next step
        :return:
        """
        print(' Agent: {}  Arrived at BaseStation {}. Battery: {} '
              .format(self.uid, self.destination, self.battery.get_charge()))
        # Update state
        if charge:
            self.state = 5
        if idle:
            self.state = 1

    def move_to(self, pos):
        """
        Move an Uav to a position
        :param pos: tuple of coordinates where the uav should move to
        """
        # Move the agent on both grids
        self.model.grid.move_agent(self, pos)

    # TODO: @Dominik what are walk lengths?
    def get_walk_lengths(self):
        """
        Get the lengths of the walks
        :return: Length of the walks
        """
        return self.walk_lengths

    # TODO: @Dominik please write a method definition (and describe what this does)
    def get_initial_delivery_distance_divided_by_average_walk_length(self):
        return self.initial_delivery_distance_divided_by_average_walk_length

    def find_uavs_close(self):
        """
        Locate UAVs that are close and exchange grids
        """
        # The worst loop ever!
        if self.model.steps <= 50:
            return

        # Scan for UAVs
        other_uavs = self.radar.scan_for_uavs(self.pos)
        # If there are other UAVs ...
        if len(other_uavs) is not 0:
            # ... exchange perceived_world_grids with them
            for other_uav in other_uavs:
                print("Agent {} and {} exchanging grid".format(self.uid, other_uav.uid))
                self.communication_module.exchange_repellents_with(other_uav)
