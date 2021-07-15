import json
import logging
import RPi.GPIO as GPIO
from serial import Serial
from .channels.pi_pico_pump import PiPicoPump
from .channels.pi_pico_analog import PiPicoAnalog
from .hardware_interface import HardwareInterface
logger = logging.getLogger(__name__)
from asyncio import Lock


class PiPico(HardwareInterface):
    lock = Lock()

    serial_no = None
    name = None

    serial_com = None
    serial = None
    interrupt = None

    channels = []

    def __init__(self, pico_config, channels=None, *args, **kwargs):
        self.config = pico_config
        # self.channels_config = pico_config['channels']
        self.serial_no = pico_config['id']
        self.interrupt = pico_config['pi_gpio_interrupt']
        # if 'serial_com' in pico_config.keys():
        #     self.serial_com = pico_config['serial_com']
        # if self.serial_com is not None:
        #     self.serial = Serial(self.serial_com, 9600, timeout=1)
        GPIO.setup(self.interrupt, GPIO.OUT)
        super(PiPico, self).__init__(self.serial_no, channels, *args, **kwargs)

    def set_serial_com(self, serial_com):
        self.serial = serial_com

    def create_channel(self):
        for channel_config in self.channels_config.values():
            if 'type' == 'pump':
                self.channels.append(PiPicoPump(self, ))

    async def send_command(self, command):
        sensor_response = {}
        await self.lock.acquire()
        try:
            self.serial.flush()
            self.serial.write(command.encode('utf-8'))
            pico_data = self.serial.readline()
            sensor_response = pico_data[:-2]
            logger.info(sensor_response)
            self.serial.flush()
        finally:
            self.lock.release()
            return sensor_response

    async def initialize(self):
        command = 'init' + "\n"
        return await self.send_command(command)
