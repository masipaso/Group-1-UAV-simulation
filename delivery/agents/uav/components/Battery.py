class Battery:
    """
    The Battery of an UAV
    """

    def __init__(self, max_charge, battery_low, battery_decrease_per_step, battery_increase_per_step):
        """
        Initialize the Battery
        :param max_charge: The maximum charge the battery can have
        :param battery_low: The threshold at which the battery charge is considered low
        :param battery_decrease_per_step: The decrease in battery charge per step
        :param battery_increase_per_step: The increase in battery charge while charging per step
        """
        self._current_charge = max_charge
        self._max_charge = max_charge
        self._battery_low = battery_low
        self._battery_decrease_per_step = battery_decrease_per_step
        self._battery_increase_per_step = battery_increase_per_step

    def charge(self):
        """
        Charge the Battery
        """
        self._current_charge += self._battery_increase_per_step

    def discharge(self):
        """
        Discharge the Battery
        """
        self._current_charge -= self._battery_decrease_per_step

    def is_low(self):
        """
        Check if the current charge of the Battery is below the threshold
        :return: True, if the charge is below the threshold, otherwise False
        """
        return True if self._current_charge < self._battery_low and self._current_charge > 0 else False

    def is_empty(self):
        """
        Check if the current charge of the Battery below or equal 0
        :return: True, if the charge is below or equal 0, otherwise False
        """
        return True if self._current_charge <= 0 else False

    def is_charged(self):
        """
        Check if the current charge of the Battery is above or equal to the max_charge
        :return: True, if the charge is above or equal the max_charge, otherwise False
        """
        return True if self._current_charge >= self._max_charge else False

    def get_charge(self):
        """
        Get the current_charge
        :return: The current_charge
        """
        return self._current_charge

    def get_max_charge(self):
        """
        Get the max charge
        :return: The max charge
        """
        return self._max_charge