import logging
from OpenHub.calibrators.raw_value_converter import RawValueConverter
from OpenHub import utilities
import time


class SoilMoistureVoltageConverter(RawValueConverter):
    logger = logging.getLogger(__name__)
    calibration_directory = None
    calibration_y_vals = [99.9, 0.01]

    def __init__(self, accessory_serial_no=None, m=None, b=None, max_voltage=0.1, min_voltage=100.0):
        self.m = m
        self.b = b
        self.max_voltage = max_voltage
        self.min_voltage = min_voltage
        self.homekit_accessory_serial_no = accessory_serial_no
        super().__init__()

    def calibrate(self, channel):
        input("Please Dry Sensor For Channel " + str(channel.index))
        for _ in range(5):
            voltage = channel.get_raw_value()
            self.set_max_voltage(voltage)
            time.sleep(1)

        input("Please Place Sensor For Channel " + str(channel.index) + " in Water")
        for _ in range(5):
            voltage = channel.get_raw_value()
            self.set_min_voltage(voltage)
            time.sleep(1)

        self.ensure_min_max_different()
        self.set_slope_and_intercept_for_calibration()

    def ensure_min_max_different(self):
        if self.max_voltage == 0:
            self.max_voltage = 3
        if self.min_voltage == 0:
            self.min_voltage = .5
        if self.max_voltage == self.min_voltage:
            self.max_voltage = self.min_voltage + .1

    def set_slope_and_intercept_for_calibration(self):
        self.logger.info("Calculating new slope and intercept for output computation")
        self.m, self.b = utilities.best_fit([(1 / self.min_voltage), (1 / self.max_voltage)], self.calibration_y_vals)

    def set_min_max_voltage(self, voltage):
        if self.set_min_voltage(voltage) or self.set_max_voltage(voltage):
            self.set_slope_and_intercept_for_calibration()

    def set_max_voltage(self, voltage):
        if voltage > self.max_voltage and voltage != self.min_voltage:
            self.logger.debug("New Maximum Voltage Found")
            self.logger.debug("Old Maximum Voltage:" + str(self.max_voltage))
            self.logger.debug("Setting maximum_voltage to: " + str(voltage))
            self.max_voltage = voltage
            return True
        return False

    def set_min_voltage(self, voltage):
        if voltage < self.min_voltage:
            self.logger.debug("New Minimum Voltage Found")
            self.logger.debug("Old Minimum Voltage:" + str(self.min_voltage))
            self.logger.debug("Setting minimum_voltage to: " + str(voltage))
            self.min_voltage = voltage
            return True
        return False

    def set_min_max_voltage_from_previous_calibration(self):
        self.set_max_voltage_from_prior_calibration()
        self.set_min_voltage_from_prior_calibration()

    def set_max_voltage_from_prior_calibration(self):
        self.logger.info("Setting max_voltage based on previous slope and intercept.")
        self.max_voltage = -(self.m / self.b)

    def set_min_voltage_from_prior_calibration(self):
        self.logger.info("Setting min_voltage based on previous slope and intercept.")
        self.min_voltage = (self.m / (100 - self.b))

    def convert_voltage_to_output(self, voltage):
        return self.m * (1 / voltage + self.b)

    def convert(self, voltage):
        output = self.convert_voltage_to_output(voltage)
        self.set_min_max_voltage(voltage)
        return output
