from Adafruit_GPIO import GPIO
from OpenHub.homekit_accessories.homkit_sensor_interface import HomeKitSensorInterface
import logging

from pyhap.const import CATEGORY_SWITCH

logger = logging.getLogger(__name__)


class Pump(HomeKitSensorInterface):
    run_debug_message = "Pump State: "


    def __init__(self, serial_no=None, display_name=None, channel_interface_serial_no=None, *args, **kwargs):
        self.category = CATEGORY_SWITCH

        super().__init__(serial_no=serial_no, display_name=display_name,
                         channel_interface_serial_no=channel_interface_serial_no, *args, **kwargs)

    def set_display_name(self, display_name):
        if self.display_name is None:
            return display_name + "Pump"

    def add_functional_service(self):
        return self.add_preload_service('Pump')

    def add_functional_service_characteristic(self):
        return self.service.configure_char(
            'On', setter_callback=self.set_pump)

    def __setstate__(self, state):
        self.__dict__.update(state)
        # self._gpio_setup(self.pin)

    def set_pump(self, value):
        if value:
            self.channel.turn_on()
        else:
            self.channel.turn_off()

    async def stop(self):
        self.channel.turn_off()
        await super().stop()

    async def run(self):
        pass
