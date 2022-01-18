import json
import logging
import RPi.GPIO as GPIO
from serial import Serial
from .channels.pi_pico_pump import PiPicoPump
from .channels.pi_pico_analog import PiPicoAnalog
from .channels.pi_pico_relay import PiPicoRelay
from .hardware_interface import HardwareInterface

logger = logging.getLogger(__name__)
from asyncio import Lock


class Pi(HardwareInterface):
    lock = Lock()

    serial_no = None

    serial = None

    channels = []

    def __init__(self, config, channels=None, *args, **kwargs):
        self.config = config

        # self.channels_config = pico_config['channels']
        self.serial_no = config['id']
        super(Pi, self).__init__(self.serial_no,  *args, **kwargs)

    @classmethod
    def _gpio_setup(_cls):
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BOARD)

    @classmethod
    def create_output_pin(_cls, pin):
        Pi._gpio_setup()
        GPIO.setup(pin, GPIO.OUT)

    @classmethod
    def create_input_pin(_cls, pin):
        Pi._gpio_setup()
        GPIO.setup(pin, GPIO.IN)