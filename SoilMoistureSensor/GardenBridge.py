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

from SoilMoistureSensor.Sensors.AirTemperatureHumiditySensor import AirTemperatureHumiditySensor
from SoilMoistureSensor.Sensors.LightSensor import LightSensor
from SoilMoistureSensor.Sensors.SoilTemperatureSensor import SoilTemperatureSensor


class GardenBridge(Bridge):
    category = CATEGORY_SENSOR
    logger = logging.getLogger(__name__)

    config_file_path = """/home/lesserdaemon/.hap-python/SoilMoistureSensor/soil_sensor.json"""
    config = {}

    garden_sensors = {}
    num_sensors = 5
    display_name = None

    serial_no = None

    air_temp_hum_present = False
    soil_temp_present = False
    light_level_present = False
    soil_moisture_present = False

    soil_temp_sensor = {}
    air_temp_humidity_sensor = {}
    light_level_sensor = {}

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
        self.setup_soil_moisture_sensors_from_local(sensor_configs)
        self.setup_air_temp_humidity_from_local(sensor_configs)
        self.setup_soil_temperature_sensor_from_local(sensor_configs)
        self.setup_light_level_sensor_from_local(sensor_configs)

    def setup_soil_moisture_sensors_from_local(self, sensor_configs):
        if "soil_moisture_sensor_configs" in sensor_configs.keys():
            soil_moisture_sensor_configs = sensor_configs["soil_moisture_sensors"]
            for index in soil_moisture_sensor_configs.keys():
                sensor_config = sensor_configs[index]
                soil_moisture_sensor = SoilMoistureSensor(self.driver, data=sensor_config)
                self.add_accessory(soil_moisture_sensor)
                self.garden_sensors[index] = soil_moisture_sensor

    def setup_light_level_sensor_from_local(self, sensor_configs):
        if "light_level_sensor" in sensor_configs.keys():
            light_level_sensor_config = sensor_configs["light_level_sensor"]
            self.light_level_sensor = LightSensor(self.driver, data=light_level_sensor_config)
            self.add_accessory(self.light_level_sensor)

    def setup_soil_temperature_sensor_from_local(self, sensor_configs):
        if "soil_temperature_sensor" in sensor_configs.keys():
            soil_temperature_sensor_config = sensor_configs["soil_temperature_sensor"]
            self.soil_temp_sensor = LightSensor(self.driver, data=soil_temperature_sensor_config)
            self.add_accessory(self.soil_temp_sensor)

    def setup_air_temp_humidity_from_local(self, sensor_configs):
        if "air_temperature_humidity_sensor" in sensor_configs.keys():
            air_temperature_humidity_sensor_config = sensor_configs["air_temperature_humidity_sensor"]
            self.air_temp_humidity_sensor = LightSensor(self.driver, data=air_temperature_humidity_sensor_config)
            self.add_accessory(self.air_temp_humidity_sensor)

    def configure_hub_first_time(self):
        self.add_name()
        self.configure_soil_moisture_sensors()
        self.configure_air_temp_humidity()
        self.configure_soil_temp()
        self.configure_light_level()
        self.serial_no = str(uuid.uuid4())
        self.config["serial_no"] = self.serial_no
        self.config["display_name"] = self.display_name

    def configure_light_level(self):
        self.light_level_present = str(input("Is a level sensor connected?")).lower() == "yes"
        self.config["light_level_present"] = self.light_level_present

    def configure_soil_temp(self):
        self.soil_temp_present = str(input("Is a soil temperature sensor connected?")).lower() == "yes"
        self.config["soil_temp_present"] = self.soil_temp_present

    def configure_air_temp_humidity(self):
        self.air_temp_hum_present = str(input("Is an air temperature/humidity sensor connected?")).lower() == "yes"
        self.config["air_temp_hum_present"] = self.air_temp_hum_present

    def configure_soil_moisture_sensors(self):
        self.soil_moisture_present = str(input("Are soil moisture sensors connected?")).lower() == "yes"

        if self.soil_moisture_present:
            self.num_sensors = int(input("How many sensors? "))
        else:
            self.num_sensors = 0
        self.config["num_sensors"] = self.num_sensors
        self.config["soil_moisture_present"] = self.soil_moisture_present

    def add_name(self):
        if self.display_name is None:
            self.display_name = input("Please Add Display Name for Garden Hub. ") or "GardenHubDisplayName"

    def configure_sensors_first_time(self):
        self.setup_soil_moisture_sensors_first_time()
        self.setup_light_sensor_first_time()
        self.setup_soil_temperature_sensor_first_time()
        self.setup_air_temp_humidity_sensor_first_time()

    def setup_light_sensor_first_time(self):
        if self.light_level_present:
            id = str(uuid.uuid4())
            sensor_config = {"serial_no": id}
            self.light_level_sensor = LightSensor(self.driver, data=sensor_config)
            self.add_accessory(self.light_level_sensor)

    def setup_air_temp_humidity_sensor_first_time(self):
        if self.air_temp_hum_present:
            id = str(uuid.uuid4())
            sensor_config = {"serial_no": id}
            self.air_temp_humidity_sensor = AirTemperatureHumiditySensor(self.driver, data=sensor_config)
            self.add_accessory(self.air_temp_humidity_sensor)

    def setup_soil_temperature_sensor_first_time(self):
        if self.soil_temp_present:
            id = str(uuid.uuid4())
            sensor_config = {"serial_no": id}
            self.soil_temp_sensor = SoilTemperatureSensor(self.driver, data=sensor_config)
            self.add_accessory(self.soil_temp_sensor)

    def setup_soil_moisture_sensors_first_time(self):
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
        soil_moisture_sensors = {}
        ind = 0
        for garden_sensor in self.garden_sensors.values():
            soil_moisture_sensors[ind] = garden_sensor.as_json()
            ind = ind + 1
        self.config["sensors"]["soil_moisture_sensors"] = soil_moisture_sensors
        self.config["sensors"]["air_temperature_humidity_sensor"] = self.air_temp_humidity_sensor.as_json()
        self.config["sensors"]["soil_temperature_sensor"] = self.soil_temp_sensor.as_json()
        self.config["sensors"]["light_level_sensor"] = self.light_level_sensor.as_json()
        self.config["aid"] = self.aid

    @Accessory.run_at_interval(5)
    async def run(self):
        await super().run()
