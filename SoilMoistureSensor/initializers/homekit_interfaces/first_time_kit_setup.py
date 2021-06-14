import uuid
import os
from SoilMoistureSensor.hardware_interfaces.channels.mod_probe_temp import ModProbeTemp
from SoilMoistureSensor.hardware_interfaces.channels.veml7700_lux import VEML7700Lux
from SoilMoistureSensor.hardware_interfaces.channels.veml7700_light import VEML7700Light
from SoilMoistureSensor.hardware_interfaces.channels.dht22_temp import DHT22Temp
from SoilMoistureSensor.hardware_interfaces.channels.dht22_humidity import DHT22Humidity
from SoilMoistureSensor.homekit_accessories.soil_moisture_sensor import SoilMoistureSensor
from SoilMoistureSensor.homekit_accessories.soil_temperature_sensor import SoilTemperatureSensor
from SoilMoistureSensor.homekit_accessories.air_temperature import AirTemperatureSensor
from SoilMoistureSensor.homekit_accessories.humidity import HumiditySensor
from SoilMoistureSensor.homekit_accessories.light_sensor import LightSensor
from SoilMoistureSensor.homekit_accessories.liquid_level_sensor import LiquidLevelSensor
from SoilMoistureSensor.homekit_accessories.pressure_sensor import PressureSensor
from SoilMoistureSensor.homekit_accessories.pump import Pump
from SoilMoistureSensor.homekit_accessories.etape import ETapeSensor

def first_run():
    initialize_homekit_interface_config()
    configure_hub_first_time()


def initialize_homekit_interface_config():
    homekit_interface_config_file = os.getenv('OPENHUB_HOMEKIT_CONFIG_FILE')
    if homekit_interface_config_file is None:
        from SoilMoistureSensor.config_files import HOMEKIT_CONFIG_FILE

        homekit_interface_config_file = input(
            "What is the absolute path you would like to set for the homekit interface config?") or HOMEKIT_CONFIG_FILE
        if homekit_interface_config_file != HOMEKIT_CONFIG_FILE:
            "Please place this in your bash_profile: export OPENHUB_HOMEKIT_CONFIG_FILE=" + homekit_interface_config_file
            HOMEKIT_CONFIG_FILE = homekit_interface_config_file
            os.putenv('HOMEKIT_CONFIG_FILE', HOMEKIT_CONFIG_FILE)
    else:
        print(
            'Setting homekit config file to environment variable OPENHUB_HOMEKIT_CONFIG_FILE: ' + homekit_interface_config_file)


def configure_hub_first_time(sensor_hub):
    sensor_hub.add_name()
    sensor_hub.configure_soil_moisture_sensors()
    sensor_hub.configure_air_temp_humidity()
    sensor_hub.configure_soil_temp()
    sensor_hub.configure_light_level()
    sensor_hub.serial_no = str(uuid.uuid4())
    sensor_hub.config["serial_no"] = sensor_hub.serial_no
    sensor_hub.config["display_name"] = sensor_hub.display_name


def add_name(sensor_hub):
    if sensor_hub.display_name is None:
        sensor_hub.display_name = input("Please Add Display Name for OpenHub: ") or "OpenHub"


def interface_channel_with_homekit_accessory(sensor_hub, channel):
    if channel.__name__ == ModProbeTemp.__name__:
        accessory = setup_soil_temperature_sensor_first_time(channel)
    elif channel.__name__ == VEML7700Lux.__name__:
        accessory = setup_light_sensor_first_time(channel)
    elif channel.__name__ == VEML7700Light.__name__:
        accessory = setup_light_sensor_first_time(channel)
    elif channel.__name__ == DHT22Temp.__name__:
        accessory = setup_air_temp_sensor_first_time(channel)
    elif channel.__name__ == DHT22Humidity.__name__:
        accessory = setup_humidity_sensor_first_time(channel)
    else:
        accessory = None
        channel_type = str(input("What type of homekit accessory should use this channel??"))
        if channel_type == 'soilmoisture':
            accessory = setup_soil_moisture_sensor_first_time(channel)
        if channel_type == 'soiltemperature':
            accessory = setup_soil_temperature_sensor_first_time(channel)
        if channel_type == 'airtemperature':
            accessory = setup_air_temp_sensor_first_time(channel)
        if channel_type == 'humidity':
            accessory = setup_humidity_sensor_first_time(channel)
        if channel_type == 'light':
            accessory = setup_light_sensor_first_time(channel)
        if channel_type == 'liquidlevel':
            accessory = setup_liquid_level_sensor_first_time(channel)
        if channel_type == 'pressure':
            accessory = setup_pressure_sensor_first_time(channel)
        if channel_type == 'etape':
            accessory = setup_etape_sensor_first_time(channel)
        if channel_type == 'pump':
            accessory = setup_pump_first_time(channel)
    if accessory is not None:
        sensor_hub.add_accessory(accessory)


def setup_light_sensor_first_time(channel):
    id = str(uuid.uuid4())
    return LightSensor(serial_no=id, channel_interface_serial_no=channel.serial_no)


def setup_air_temp_sensor_first_time(channel):
    id = str(uuid.uuid4())
    return AirTemperatureSensor(serial_no=id, channel_interface_serial_no=channel.serial_no)


def setup_humidity_sensor_first_time(channel):
    id = str(uuid.uuid4())
    return HumiditySensor(serial_no=id, channel_interface_serial_no=channel.serial_no)


def setup_soil_temperature_sensor_first_time(channel):
    id = str(uuid.uuid4())
    return SoilTemperatureSensor(serial_no=id, channel_interface_serial_no=channel.serial_no)


def setup_soil_moisture_sensor_first_time(channel):
    id = str(uuid.uuid4())
    return SoilMoistureSensor(serial_no=id, channel_interface_serial_no=channel.serial_no)


def setup_etape_sensor_first_time(channel):
    id = str(uuid.uuid4())
    return ETapeSensor(serial_no=id, channel_interface_serial_no=channel.serial_no)


def setup_liquid_level_sensor_first_time(channel):
    id = str(uuid.uuid4())
    return LiquidLevelSensor(serial_no=id, channel_interface_serial_no=channel.serial_no)


def setup_pressure_sensor_first_time(channel):
    id = str(uuid.uuid4())
    return PressureSensor(serial_no=id, channel_interface_serial_no=channel.serial_no)


def setup_pump_first_time(channel):
    id = str(uuid.uuid4())
    return Pump(serial_no=id, channel_interface_serial_no=channel.serial_no)
