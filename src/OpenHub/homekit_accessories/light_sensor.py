from pyhap.const import CATEGORY_SENSOR
import logging
import OpenHub.hardware_interfaces.veml_7700 as veml
from OpenHub.homekit_accessories.homkit_sensor_interface import HomeKitSensorInterface


class LightSensor(HomeKitSensorInterface):
    logger = logging.getLogger(__name__)
    run_debug_message = "Current Light Level: "


    index = None
    channel = None
    light_service = None
    light_service2 = None
    char_ambient = None
    char_lux = None
    category = CATEGORY_SENSOR
    serial_no = None
    name = None
    display_name = None

    def __init__(self, serial_no=None, display_name=None, channel_interface_serial_no=None, *args, **kwargs):
        if self.display_name is None:
            self.display_name = display_name + "LightSensor"
        super().__init__(serial_no=serial_no, display_name=display_name,
                         channel_interface_serial_no=channel_interface_serial_no, *args, **kwargs)

    def set_display_name(self, display_name):
        if display_name is None:
            return "Light Sensor"
        else:
            return display_name


    def add_functional_service(self):
        return self.add_preload_service("LightSensor")

    def add_functional_service_characteristic(self):
        return self.service.get_characteristic('CurrentAmbientLightLevel')

