import json
from SoilMoistureSensor.hardware_interfaces.json import hardware_interface_decoder
from SoilMoistureSensor.homekit_accessories.json import homekit_decoder
from SoilMoistureSensor.calibrators.json import raw_value_decoder
from SoilMoistureSensor.config_files import HARDWARE_CONFIG_FILE, HOMEKIT_CONFIG_FILE, CALIBRATION_CONFIG_FILE


def load_hardware_config():
    global hardware
    hardware = json.load(open(HARDWARE_CONFIG_FILE), cls=hardware_interface_decoder.HardwareDecoder)


def load_homekit_accessory_config():
    global accessories
    accessories = json.load(open(HOMEKIT_CONFIG_FILE), cls=homekit_decoder.HomekitDecoder)


def load_calibration_config():
    global calibration
    calibration = json.load(open(CALIBRATION_CONFIG_FILE), cls=raw_value_decoder.RawValueDecoder)


def load_configs():
    load_hardware_config()
    load_homekit_accessory_config()
    load_calibration_config()


