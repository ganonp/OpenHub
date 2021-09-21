import asyncio

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
        if display_name is None:
            return "Pump"
        else:
            return display_name

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
            asyncio.create_task(self.channel.turn_on_lock(self.channel.pipico.lock))
        else:
            asyncio.create_task(self.channel.turn_off_lock(self.channel.pipico.lock))


    async def stop(self):
        await self.channel.turn_off()
        await super().stop()

    async def run(self):
        pass
