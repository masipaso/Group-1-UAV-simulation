import unittest
from delivery.agents.uav.components.Battery import Battery


class BatteryTest(unittest.TestCase):
    def setUp(self):
        self.battery = Battery(max_charge=1000, battery_low=500, battery_decrease_per_step=1, battery_increase_per_step=10)

    def test_init(self):
        self.assertEqual(self.battery._current_charge, 1000)
        self.assertEqual(self.battery._max_charge, 1000)
        self.assertEqual(self.battery._battery_low, 500)
        self.assertEqual(self.battery._battery_decrease_per_step, 1)
        self.assertEqual(self.battery._battery_increase_per_step, 10)

    def test_charge(self):
        # Test: After charge() battery charge should be increased by 10, i.e. equal 1010
        self.battery.charge()
        self.assertEqual(self.battery._current_charge, 1010)

    def test_discharge(self):
        # Test: After discharge battery charge should be decreased by 1, i.e. equal 999
        self.battery.discharge()
        self.assertEqual(self.battery._current_charge, 999)

    def test_is_low(self):
        # 1st Test: 0 < charge > battery_low, result: false
        self.battery._current_charge = 1000
        self.assertFalse(self.battery.is_low())

        # 2nd Test: 0 < charge < battery_low, result: True
        self.battery._current_charge = 499
        self.assertTrue(self.battery.is_low())

    def test_is_empty(self):
        # 1st Test: 0 < charge, result: false
        self.assertFalse(self.battery.is_empty())

        # 2nd Test: 0 = charge, result: True
        self.battery._current_charge = 0
        self.assertTrue(self.battery.is_empty())

        # 3rd Test: 0 > charge, result: True
        self.battery._current_charge = -1
        self.assertTrue(self.battery.is_empty())

    def test_is_charged(self):
        # 1st Test: charge = max_charge (as initialized), result: True
        self.assertTrue(self.battery.is_charged())

        # 2nd Test: charge > max_charge, result: True
        self.battery._current_charge = 10000
        self.assertTrue(self.battery.is_charged())

        # 3rd Test: charge < max_charge, result: False
        self.battery._current_charge = 100
        self.assertFalse(self.battery.is_charged())

    def test_get_charge(self):
        # Test: get_charge() = current_charge
        self.assertEqual(self.battery.get_charge(), self.battery._current_charge)
