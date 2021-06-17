import json
from OpenHub.hardware_interfaces.json.hardware_interface_encoder import HardwareEncoder
from OpenHub.homekit_accessories.json.homekit_encoder import HomekitEncoder
from OpenHub.calibrators.json.raw_value_encoder import RawValueEncoder
from OpenHub.config_files import HARDWARE_CONFIG_FILE, HOMEKIT_CONFIG_FILE, CALIBRATION_CONFIG_FILE
from OpenHub.globals import accessories, id_hardware_map, calibration


def write_hardware_config():
    global hardware
    json.dump(hardware, fp=HARDWARE_CONFIG_FILE, cls=HardwareEncoder)


def write_homekit_accessory_config():
    global accessories
    json.dump(open(HOMEKIT_CONFIG_FILE), fp=HOMEKIT_CONFIG_FILE, cls=HomekitEncoder)


def load_calibration_config():
    global calibration
    json.load(open(CALIBRATION_CONFIG_FILE), fp=CALIBRATION_CONFIG_FILE, cls=RawValueEncoder)


def write_configs():
    write_hardware_config()
    write_homekit_accessory_config()
    load_calibration_config()


