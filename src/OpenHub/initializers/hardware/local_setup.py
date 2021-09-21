from OpenHub.globals import id_hardware_map
from hardware_interfaces.json import HardwareDecoder
import json


def configure_hardware_from_local(sensor_hub):
    components = sensor_hub.config["hardware"]
    for component in components:
        comp = json.loads(component, cls=HardwareDecoder)
        id_hardware_map.append(comp)
