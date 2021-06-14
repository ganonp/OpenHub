from pyhap.const import CATEGORY_SENSOR
from pyhap.accessory import Accessory
import logging
import SoilMoistureSensor.hardware_interfaces.veml_7700 as veml
from SoilMoistureSensor.homekit_accessories.homkit_sensor_interface import HomeKitSensorInterface


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
        self.from_json(kwargs["data"])
        if self.display_name is None:
            self.display_name = display_name + "LightSensor"
        super().__init__(serial_no=serial_no, display_name=display_name,
                         channel_interface_serial_no=channel_interface_serial_no, *args, **kwargs)

    def set_display_name(self, display_name):
        if self.display_name is None:
            return display_name + "LightSensor"

    def add_functional_service(self):
        return self.add_preload_service("LightSensor")

    def add_functional_service_characteristic(self):
        return self.service.get_characteristic('CurrentAmbientLightLevel')

    async def run(self):
        light = veml.veml7700.light
        lux = veml.veml7700.lux
        self.char_ambient.set_value(lux)
        self.logger.debug("Current light: " + str(light))
        self.logger.debug("Current lux: " + str(lux))
