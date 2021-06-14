from pyhap.const import CATEGORY_SENSOR
from pyhap.accessory import Accessory
import logging
from SoilMoistureSensor.homekit_accessories.homkit_sensor_interface import HomeKitSensorInterface


class SoilTemperatureSensor(HomeKitSensorInterface):
    logger = logging.getLogger(__name__)
    index = None
    run_debug_message = "Current Soil Temperature: "

    def __init__(self, serial_no=None, display_name=None, channel_interface_serial_no=None, *args, **kwargs):
        self.from_json(kwargs["data"])
        if self.display_name is None:
            self.display_name = display_name + "SoilTemperature"
        super().__init__(serial_no=serial_no, display_name=display_name,
                         channel_interface_serial_no=channel_interface_serial_no, *args, **kwargs)

    def set_display_name(self, display_name):
        if self.display_name is None:
            return display_name + "SoilTemperature"

    def add_functional_service(self):
        return self.add_preload_service("TemperatureSensor")

    def add_functional_service_characteristic(self):
        return self.service.get_characteristic('CurrentTemperature')

    # async def run(self):
    #     try:
    #         self.char.set_value(modProbe.read_temp_c())
    #     except IndexError as e:
    #         self.logger.warning(str(e))
