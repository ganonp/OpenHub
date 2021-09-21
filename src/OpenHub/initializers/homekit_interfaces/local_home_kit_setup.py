from pyhap.const import STANDALONE_AID
from OpenHub.globals import id_hardware_map
from OpenHub.homekit_accessories.json import HomekitDecoder
import json


def configure_hub_from_local(sensor_hub):
    config_file = open(sensor_hub.config_file_path, "r")
    sensor_hub.config = json.load(config_file)
    config_file.close()

    sensor_hub.serial_no = sensor_hub.config["serial_no"]
    sensor_hub.aid = sensor_hub.config["aid"] or STANDALONE_AID
    sensor_hub.display_name = sensor_hub.config["display_name"] or "OpenHub"


def configure_accessories_from_local(sensor_hub):
    components = sensor_hub.config["accessories"]
    for component in components:
        comp = json.loads(component, cls=HomekitDecoder)
        id_hardware_map.append(comp)
