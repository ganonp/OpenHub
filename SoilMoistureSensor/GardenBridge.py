import logging

import os
import json
import uuid
from SoilMoistureSensor.Sensors import SoilMoistureSensor
from SoilMoistureSensor.HardwareInterfaces import MCPInterface as mcpi

from pyhap.const import CATEGORY_SENSOR
from pyhap.accessory import Bridge
from pyhap.accessory import Accessory
from pyhap.const import STANDALONE_AID


class GardenBridge(Bridge):
    category = CATEGORY_SENSOR
    logger = logging.getLogger(__name__)

    config_file_path = """/home/lesserdaemon/.hap-python/SoilMoistureSensor/soil_sensor.json"""
    config = {}

    garden_sensors = {}
    num_sensors = 5
    display_name = None

    serial_no = None

    def __init__(self, driver, **kwargs):
        self.configure_hub()
        super().__init__(driver, self.display_name)
        self.configure_sensors()

    def configure_hub(self):
        if os.path.exists(self.config_file_path):
            self.configure_hub_from_local()
        else:
            self.configure_hub_first_time()
        mcpi.setup(self.num_sensors)

    def configure_sensors(self):
        if os.path.exists(self.config_file_path):
            self.configure_sensors_from_local()
        else:
            self.configure_sensors_first_time()
            self.save()

    def configure_hub_from_local(self):
        config_file = open(self.config_file_path, "r")
        self.config = json.load(config_file)
        config_file.close()

        self.num_sensors = self.config["num_sensors"]
        self.serial_no = self.config["serial_no"]
        self.serial_no = self.config["aid"] or STANDALONE_AID
        self.display_name = self.config["display_name"] or "GardenHubDisplayName"

    def configure_sensors_from_local(self):
        sensor_configs = self.config["sensors"]
        for index in sensor_configs.keys():
            sensor_config = sensor_configs[index]
            soil_moisture_sensor = SoilMoistureSensor(self.driver, data=sensor_config)
            self.add_accessory(soil_moisture_sensor)
            self.garden_sensors[index] = soil_moisture_sensor

    def configure_hub_first_time(self):
        self.add_name()
        self.num_sensors = int(input("How many sensors? "))
        self.config["num_sensors"] = self.num_sensors
        self.serial_no = str(uuid.uuid4())
        self.config["serial_no"] = self.serial_no
        self.config["display_name"] = self.display_name

    def add_name(self):
        if self.display_name is None:
            self.display_name = input("Please Add Display Name for Garden Hub. ") or "GardenHubDisplayName"

    def configure_sensors_first_time(self):
        for ind in range(self.num_sensors):
            id = str(uuid.uuid4())
            sensor_config = {"serial_no": id, "index": ind}
            soil_moisture_sensor = SoilMoistureSensor(self.driver, data=sensor_config)
            self.add_accessory(soil_moisture_sensor)
            self.garden_sensors[ind] = soil_moisture_sensor
            self.garden_sensors[ind].calibrate()

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
        sensors = {}
        ind = 0
        for garden_sensor in self.garden_sensors.values():
            sensors[ind] = garden_sensor.as_json()
            ind = ind + 1
        self.config["sensors"] = sensors
        self.config["aid"] = self.aid

    @Accessory.run_at_interval(5)
    async def run(self):
        await super().run()
