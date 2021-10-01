import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C




import logging
from OpenHub.hardware_interfaces import hardware_interface
from OpenHub.hardware_interfaces.channels.mcp3008analog import MCP3008Analog


class MCP3008(hardware_interface.HardwareInterface):
    logger = logging.getLogger(__name__)

    reset_pin = None

    # If you have a GPIO, its not a bad idea to connect it to the RESET pin
    # reset_pin = DigitalInOut(board.G0)
    # reset_pin.direction = Direction.OUTPUT
    # reset_pin.value = False

    def __init__(self, scl=board.SCL, sda=board.SDA, serial_no=None, channels=None, reset_pin_num=board.G0, *args, **kwargs):
        reset_pin = DigitalInOut(reset_pin_num)
        reset_pin.direction = Direction.OUTPUT
        reset_pin.value = False
        i2c = busio.I2C(scl, sda, frequency=100000)
        # Connect to a PM2.5 sensor over I2C
        pm25 = PM25_I2C(i2c, reset_pin)
        self.type = __name__
        super().__init__(serial_no, channels, *args, **kwargs)

    def create_channel(self):
        pin = str(input("Which channel is this (0-8)?"))
        return self.create_analog_channel(pin)


