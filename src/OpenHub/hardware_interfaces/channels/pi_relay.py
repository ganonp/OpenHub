from .channel_interface import ChannelInterface
import logging
from OpenHub.globals import id_hardware_map
import json
import RPi.GPIO as GPIO
from OpenHub.hardware_interfaces.pi import Pi

class PiRelay(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, config, hardware_serial_no=None, serial_no=None, *args, **kwargs):
        self.serial_no = config['id']
        self.type = config['type']

        super().__init__(config=config, serial_no=self.serial_no, *args, **kwargs)

    def setup(self,pin):
        self.pin = pin
        Pi.create_output_pin(self.pin)

    async def turn_on(self):
        GPIO.output(self.pin, 1)


    async def turn_off(self):
        GPIO.output(self.pin, 0)

    async def get_raw_data(self):
        pass