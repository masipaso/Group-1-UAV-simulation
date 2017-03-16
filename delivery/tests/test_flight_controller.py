import unittest
from delivery.agents.uav.Uav import Uav
from delivery.agents.BaseStation import BaseStation
from delivery.model.Worldmodel import WorldModel

# Only testing move_to method here, as it can be predicted. The other implementations are left to you! Implement
# make_step() for the actual algorithm that you implement!


class FlightControllerTest(unittest.TestCase):

    def setUp(self):
        self.model = WorldModel()
        self.base_station = BaseStation(model=self.model, pos=(200, 200, 200), bid=1, center=(200, 200, 200),
                                        range_of_base_station=250)
        pos_x, pos_y, pos_z = self.base_station.get_pos()
        # Create the UAV
        position = (pos_x, pos_y, pos_z)

        self.uav = Uav(self.model, pos=position, uid=2, max_charge=1000, battery_low=500,
                       base_station=self.base_station, battery_decrease_per_step=1,
                       battery_increase_per_step=10, max_altitude=4, sensor_range=5)

        self.flight_controller = self.uav.flight_controller

    def test_init(self):
        self.assertEqual(self.flight_controller.visited_cells, [])
        self.assertIsNone(self.flight_controller.current_best_cell)
        self.assertEqual(self.flight_controller.current_path, [])

    def test_move_to(self):
        self.flight_controller.move_to((30, 30, 1))
        self.assertEqual(self.uav.pos, (30, 30, 1))
