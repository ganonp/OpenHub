import logging
import RPi.GPIO as GPIO
import json
from hardware_interfaces import mcp3008 as mcpi

from pyhap.const import CATEGORY_SENSOR
from pyhap.accessory import Bridge
from pyhap.accessory import Accessory

import initializers.hardware.local_setup as local_setup
from initializers.hardware import first_time_setup

import os


class GardenBridge(Bridge):
    category = CATEGORY_SENSOR
    logger = logging.getLogger(__name__)

    config_file_path = """/home/lesserdaemon/.hap-python/OpenHub/soil_sensor.json"""
    config = {}

    garden_sensors = {}
    num_sensors = 5
    display_name = None

    serial_no = None

    air_temp_hum_present = False
    soil_temp_present = False
    light_level_present = False
    soil_moisture_present = False

    soil_temp_sensor = None
    air_temp_humidity_sensor = None
    light_level_sensor = None

    @classmethod
    def _gpio_setup(_cls, pin):
        if GPIO.mode() is None:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

    def __init__(self, driver, **kwargs):
        self.configure_hub()
        super().__init__(driver, self.display_name)
        self.configure_sensors()

    def configure_hub(self):
        if os.path.exists(self.config_file_path):
            local_setup.configure_hub_from_local(self)
        else:
            first_time_setup.configure_hub_first_time(self)
        mcpi.setup(self.num_sensors)

    def configure_sensors(self):
        if os.path.exists(self.config_file_path):
            local_setup.configure_sensors_from_local(self)
        else:
            first_time_setup.configure_sensors_first_time(self)
            self.save()

    def add_info_service(self):
        """Helper method to add the required `AccessoryInformation` service.

        Called in `__init__` to be sure that it is the first service added.
        May be overridden.
        """
        serv_info = self.driver.loader.get_service("AccessoryInformation")
        serv_info.configure_char("Name", value=self.display_name)
        serv_info.configure_char("Manufacturer", value="BellyFrito")
        serv_info.configure_char("Model", value="GardenBridge")
        serv_info.configure_char("SerialNumber", value=self.serial_no)
        self.add_service(serv_info)

    def add_garden_hub_service(self):
        serv_info = self.driver.loader.get_service("GardenHub")
        serv_info.configure_char("IsConfigured", False)

        self.add_service(serv_info)

    def calibrate_sensor(self, index):
        self.garden_sensors[index].calibrate()

    def calibrate(self):
        for key in self.garden_sensors.keys():
            self.garden_sensors[key].calibrate()

    def save(self):
        self.update_config_sensors()

        with open(self.config_file_path, 'w') as file:
            file.write(json.dumps(self.config))
            file.close()

    def update_config_sensors(self):
        self.config["sensors"] = {}
        soil_moisture_sensors = {}
        ind = 0
        for garden_sensor in self.garden_sensors.values():
            soil_moisture_sensors[ind] = garden_sensor.as_json()
            ind = ind + 1
        self.config["sensors"]["soil_moisture_sensors"] = soil_moisture_sensors
        if self.air_temp_humidity_sensor is not None:
            self.config["sensors"]["air_temperature_humidity_sensor"] = self.air_temp_humidity_sensor.as_json()
        if self.soil_temp_sensor is not None:
            self.config["sensors"]["soil_temp_sensor"] = self.soil_temp_sensor.as_json()
        if self.light_level_sensor is not None:
            self.config["sensors"]["light_level_sensor"] = self.light_level_sensor.as_json()
        if first_time_setup.picos is not None:
            self.config["sensors"]["picos"] = first_time_setup.pico_configs
        self.config["aid"] = self.aid

    @Accessory.run_at_interval(5)
    async def run(self):
        await super().run()
