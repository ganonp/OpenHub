from pyhap.const import CATEGORY_SENSOR
from pyhap.accessory import Accessory
import time
import Utilities
import logging
import MCPInterface as mcpi


class SoilMoistureSensor(Accessory):
    logger = logging.getLogger(__name__)
    index = None
    channel = None
    moisture_service = None
    char_relative_humidity = None
    m = None
    b = None
    calibration_y_vals = [99.9, 0.01]
    max_voltage = 0.1
    min_voltage = 100.0
    category = CATEGORY_SENSOR
    serial_no = None
    name = None
    display_name = None

    def __init__(self, driver, **kwargs):
        self.from_json(kwargs["data"])
        self.add_name()
        super().__init__(driver, self.display_name)
        self.add_moisture_service()

    def as_json(self):
        sensor_dict = {"name": self.name, "index": self.index, "aid": self.aid, "serial_no": self.serial_no,
                       "m": self.m, "b": self.b,
                       "max_voltage": self.max_voltage, "min_voltage": self.min_voltage,
                       "display_name": self.display_name}
        return sensor_dict

    def from_json(self, data):
        if "m" in data.keys():
            self.m = data["m"]
        if "b" in data.keys():
            self.b = data["b"]
        if "min_voltage" in data.keys():
            self.min_voltage = data["min_voltage"]
        else:
            if self.m is not None and self.b is not None:
                self.set_min_voltage_from_prior_calibration()
            else:
                self.min_voltage = 100.0
        if "max_voltage" in data.keys():
            self.max_voltage = data["max_voltage"]
        else:
            if self.m is not None and self.b is not None:
                self.set_max_voltage_from_prior_calibration()
            else:
                self.max_voltage = 0.1
        if "serial_no" in data.keys():
            self.serial_no = data["serial_no"]
        if "index" in data.keys():
            self.index = data["index"]
        if "name" in data.keys():
            self.name = data["name"]
        if "aid" in data.keys():
            self.aid = data["aid"]
        if "display_name" in data.keys():
            self.display_name = data["display_name"]

    def add_name(self):
        if self.display_name is None:
            self.display_name = input(
                "Please Add Display Name for Sensor on Channel: " + str(self.index)) or "SoilMoistureDisplayName" + str(
                self.index)

    def calibrate(self):
        input("Please Dry Sensor For Channel " + str(self.index))
        for _ in range(5):
            voltage = mcpi.get_voltage_for_channel(int(self.index))
            self.set_max_voltage(voltage)
            time.sleep(1)

        input("Please Place Sensor For Channel " + str(self.index) + " in Water")
        for _ in range(5):
            voltage = mcpi.get_voltage_for_channel(int(self.index))
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
        self.m, self.b = Utilities.best_fit([(1 / self.min_voltage), (1 / self.max_voltage)], self.calibration_y_vals)

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

    def convert_voltage_to_output(self):
        return self.m * (1 / mcpi.get_voltage_for_channel(int(self.index))) + self.b

    def add_info_service(self):

        serv_info = self.driver.loader.get_service("AccessoryInformation")
        serv_info.configure_char("Name", value=self.display_name)
        serv_info.configure_char("SerialNumber", value=self.serial_no)
        serv_info.configure_char("Manufacturer", value="BellyFrito")
        serv_info.configure_char("Model", value="SoilMoistureSensor")
        self.add_service(serv_info)

    def add_moisture_service(self):

        self.moisture_service = self.add_preload_service("SoilMoistureSensor")
        self.soil_moisture = self.moisture_service.configure_char("SoilMoisture")
        # if self.name is not None:
        #     self.moisture_service.char_name = self.moisture_service.configure_char('Name', value=self.name)

    async def run(self):
        voltage = mcpi.get_voltage_for_channel(int(self.index))
        self.logger.debug("Voltage: " + str(voltage))
        self.set_min_max_voltage(voltage)
        output = self.convert_voltage_to_output()
        self.logger.debug("Output / Moisture Level: " + str(output))
        self.soil_moisture.set_value(output)
        # await asyncio.sleep(1)
