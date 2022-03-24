import board
from adafruit_motorkit import MotorKit
from .hardware_interface import HardwareInterface
import busio

class AdafruitStepperMotorHAT(HardwareInterface):

    def __init__(self, scl=board.SCL, sda=board.SDA, serial_no=None, channels=None, *args, **kwargs):
        self.i2c = busio.I2C(scl, sda)
        self.kit = MotorKit(i2c=self.i2c)
        self.type = __name__
        super().__init__(serial_no, channels, *args, **kwargs)