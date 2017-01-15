from delivery.agents.repellent import Repellent
# Import utils
from delivery.utils.step import Step
from delivery.utils.get_step_distance import get_step_distance


class FlightController:
    """
    The FlightController decides where to fly next
    """
    # TODO: More details

    def __init__(self, uav):
        """
        Initialize the FlightController
        :param uav: The UAV to which the FlightController belongs
        """
        self.uav = uav

    def make_step(self):
        """
        Advance the UAV by one step
        """
        # If the Uav does not have a destination, do nothing
        if self.uav.destination is None:
            print(' Agent: {} has no destination.'.format(self.uav.uid))
            return None

        # Get all available steps
        available_steps = self.get_available_steps()
        # If there are no available steps, do nothing
        if len(available_steps) is 0:
            print(' Agent: {} has no available steps.'.format(self.uav.uid))
            return None

        # Get all possible steps based on the available steps
        possible_steps = self.get_possible_steps(available_steps)
        # If there are no possible steps, do nothing
        if len(possible_steps) is 0:
            print(' Agent: {} has no possible steps.'.format(self.uav.uid))
            return None

        # Store the current position of the UAV to access it later
        last_position = self.uav.pos
        # New position of the UAV
        new_position = None

        # Pick the first of all possible Steps because they are sorted based on their distance to the destination
        # TODO: Make this more simple; something like possible_steps[0]?
        for possible_step in possible_steps:
            new_position = possible_step.pos
            if new_position is not 0:
                break

        # Move UAV
        self.uav.move_to(new_position)
        new_distance = self.uav.get_euclidean_distance(self.uav.pos, self.uav.destination)
        print(' Agent: {}  Moves from {} to {}. Distance to Destination: {}. Battery: {}'
              .format(self.uav.uid, last_position, new_position, new_distance, self.uav.battery.get_charge()))

        # Adding the new position to the walk
        self.uav.walk.append((new_position, new_distance))
        self.uav.real_walk.append((new_position, new_distance))
        # Iterate through the walk in reverse order to find inconsistencies
        for index, step_taken in enumerate(reversed(self.uav.walk)):
            # If the step is further away than the position on which the Uav planted the last repellent, break
            if index > self.uav.last_repellent:
                break
            # Compare the expected distance to the actual distance
            # Expected distance: amount of cells crossed to get to the current location
            expected_distance = get_step_distance(new_position, step_taken[0])
            # Actual distance: number of walk entries from the current position to the step_taken
            actual_distance = index
            # If the expected_distance is smaller than the actual_distance a suboptimal route was found
            if expected_distance < actual_distance:
                print("Path was longer than expected!")
                # If there is already a repellent on that position ...
                repellent = self.uav.perceived_grid.get_repellent_on(last_position)
                if repellent is not None:
                    # ... increase its effect
                    print("There is already a repellent on that pos - increasing its effect!")
                    repellent.strengthen()
                else:
                    # ... or create a new one
                    print("There is no repellent on that pos - creating one!")
                    repellent = Repellent(self.uav.model, last_position, self.uav.perceived_grid)
                    self.uav.perceived_grid.place_agent(repellent, last_position)
                    self.uav.walk.remove(self.uav.walk[index])
                break

    def get_possible_steps(self, available_steps):
        """
        Compute the possible steps based on the available steps
        :param available_steps: A list of available steps
        :return: a sorted list of Steps
        """
        possible_steps = []

        for available_step in available_steps:
            # Only add an available_step to the possible_steps if there is no Repellent or Obstacle at the position

            # Check the landscape
            # ... if there is no Obstacle
            if not self.uav.model.landscape.is_obstacle_at(available_step.pos):
                # ... then there might be a BaseStation (2) or nothing (0)
                # If there is a BaseStation, add the step to the possible_steps
                if self.uav.model.landscape.is_base_station_at(available_step.pos):
                    possible_steps.append(available_step)
                # ... in any other case, query the perceived grid of the UAV for Repellent information
                else:
                    # If there is something at that position
                    if not self.uav.perceived_grid.is_cell_empty(available_step.pos):
                        cell_contents = self.uav.perceived_grid.get_cell_list_contents([available_step.pos])
                        possible = []
                        # ... check the content
                        for obstacle in cell_contents:
                            # If there is a Repellent
                            if type(obstacle) is Repellent:
                                # ... the Uav might go there based on the strength and the possible decrease in distance
                                weighted_distance = available_step.distance + (available_step.distance *
                                                                               obstacle.strength / 100)
                                available_step.distance = weighted_distance
                                # Add the step with the weighted_distance to the possible_steps
                                possible.append(True)
                            else:
                                possible.append(True)
                        # If there is one reason to add the available_step to the possible_steps, do it
                        if True in possible:
                            possible_steps.append(available_step)
                    else:
                        possible_steps.append(available_step)

        # Sort all possible steps to adjust the order for weighted distances
        possible_steps.sort(key=lambda step: step.distance)
        return possible_steps

    def get_available_steps(self):
        """
        Get all available steps the UAV _could_ take
        :return: a list of Steps
        """
        # Get the neighboring cells of the grid
        neighborhood = self.uav.perceived_grid.get_neighborhood(
            self.uav.pos,
            moore=True,
            include_center=False,
            radius=1)

        available_steps = []

        # Iterate over the neighboring cells and create Steps
        for coordinates in neighborhood:
            distance = self.uav.get_euclidean_distance(self.uav.destination, coordinates)
            available_step = Step(distance=distance, pos=coordinates)
            available_steps.append(available_step)

        return available_steps
