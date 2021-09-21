import board
import busio
import adafruit_veml7700
from .hardware_interface import HardwareInterface
from .channels.veml7700_light import VEML7700Light
from .channels.veml7700_lux import VEML7700Lux


class VEML7700(HardwareInterface):

    def __init__(self, scl=board.SCL, sda=board.SDA, serial_no=None, channels=None, *args, **kwargs):
        self.i2c = busio.I2C(scl, sda)
        self.veml7700 = adafruit_veml7700.VEML7700(self.i2c)
        self.type = self.__name__
        super().__init__(serial_no, channels, *args, **kwargs)

    def create_channel(self):
        return {"light": VEML7700Light(veml=self.veml7700, hardware_serial_no=self.serial_no),
                "lux": VEML7700Lux(veml=self.veml7700, hardware_serial_no=self.serial_no)}
