from delivery.agents.repellent import Repellent
from delivery.agents.obstacle import Obstacle
from delivery.utils.step import Step


class Algorithm:
    """
    Class representing the current algorithm which is used to advance a Uav at each step
    """
    def __init__(self, uav):
        self.uav = uav

    def get_possible_steps(self):
        """
        Compute the possible steps based on the available steps
        :return: a list of Steps
        """
        available_steps = self.get_available_steps
        possible_steps = []

        for available_step in available_steps:
            # Only add an available_step to the possible_steps if there is no Repellent or Obstacle at the position
            # Check for the real world
            if not self.uav.model.grid.is_cell_empty(available_step.pos):
                cell_contents = self.uav.model.grid.get_cell_list_contents([available_step.pos])
                possible = []
                for obstacle in cell_contents:
                    if type(obstacle) is Obstacle:
                        # If there is an Obstacle the Uav cant go there
                        possible.append(False)
                    else:
                        # If there is a BaseStation or a Uav
                        possible.append(True)
                # If there is one reason to add the available_step to the possible_steps, do it
                if True in possible:
                    possible_steps.append(available_step)
            # Check for the perceived world
            elif not self.uav.model.perceived_world_grid.is_cell_empty(available_step.pos):
                cell_contents = self.uav.model.perceived_world_grid.get_cell_list_contents([available_step.pos])
                possible = []
                for obstacle in cell_contents:
                    if type(obstacle) is Obstacle:
                        # If there is an Obstacle the Uav cant go there
                        possible.append(False)
                    elif type(obstacle) is Repellent:
                        # If there is a Repellent the Uav might go there based on the strength and the possible
                        # decrease in distance
                        weighted_distance = available_step.distance + (available_step.distance * obstacle.strength / 100)
                        available_step.distance = weighted_distance
                        # In theory, the Uav can go there
                        possible.append(True)
                    else:
                        # If there is a BaseStation or a Uav
                        possible.append(True)
                # If there is one reason to add the available_step to the possible_steps, do it
                if True in possible:
                    possible_steps.append(available_step)
            else:
                possible_steps.append(available_step)

        # Sort all possible steps to adjust the order for weighted distances
        possible_steps.sort(key=lambda step: step.distance)
        return possible_steps

    @property
    def get_available_steps(self):
        """
        Get all available steps in the real world and the perceived world
        :return: a list of Steps
        """
        # Get the cells of the real world as these contain all available cells
        neighborhood_real_world = self.uav.model.grid.get_neighborhood(
            self.uav.pos,
            moore=True,
            include_center=False,
            radius=1)

        available_steps = []

        for cell in neighborhood_real_world:
            distance = self.uav.get_euclidean_distance(self.uav.destination, cell)
            available_step = Step(distance=distance, pos=cell)
            available_steps.append(available_step)

        available_steps.sort(key=lambda step: step.distance)

        return available_steps

    @staticmethod
    def get_step_distance(pos1, pos2):
        """
        Calculate the step distance between two positions
        :param pos1:
        :param pos2:
        :return: the step distance
        """
        if pos1 == pos2:
            return 0
        else:
            x = abs(pos1[0] - pos2[0])
            y = abs(pos1[1] - pos2[1])
            return max(x, y)

    def run(self):
        """
        TODO: Description
        :return:
        """
        if self.uav.destination is None:
            # If the Uav does not have a destination, do nothing but wait
            return None

        # Get all possible steps
        possible_steps = self.get_possible_steps()
        # Store the current position of the Uav to access it later
        last_position = self.uav.pos

        if possible_steps is None:
            print("no next steps")
            return
        else:
            # Pick the first of all possible steps because they are sorted based on their distance to the destination
            new_position = None
            for possible_step in possible_steps:
                new_position = possible_step.pos
                if new_position is not 0:
                    break

            # Move Uav
            self.uav.move_to(new_position)
            new_distance = self.uav.get_euclidean_distance(self.uav.pos, self.uav.destination)
            print(' Agent: {}  Moves from {} to {}. Distance to Destination: {}. Battery: {}'.format(self.uav.id, last_position,
                                                                                        new_position, new_distance, self.uav.current_charge))

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
                expected_distance = self.get_step_distance(new_position, step_taken[0])
                # Actual distance: number of walk entries from the current position to the step_taken
                actual_distance = index
                # If the expected_distance is smaller than the actual_distance a suboptimal route was found
                if expected_distance < actual_distance:
                    print("Path was longer than expected!")
                    # If there is already a repellent on that position ...
                    repellent = self.uav.model.perceived_world_grid.get_repellent_on(last_position)
                    if repellent is not None:
                        # ... increase its effect
                        print("There is already a repellent on that pos - increasing its effect!")
                        repellent.strengthen()
                    else:
                        # ... or create a new one
                        print("There is no repellent on that pos - creating one!")
                        repellent = Repellent(self.uav.model, last_position)
                        self.uav.model.perceived_world_grid.place_agent(repellent, last_position)
                        self.uav.walk.remove(self.uav.walk[index])
                    break
