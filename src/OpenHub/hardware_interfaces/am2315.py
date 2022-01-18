import logging
from OpenHub.hardware_interfaces import hardware_interface
from OpenHub.hardware_interfaces.channels.dht22_humidity import DHT22Humidity
from OpenHub.hardware_interfaces.channels.dht22_temp import DHT22Temp
import board
import busio
import adafruit_am2320


class AM2315(hardware_interface.HardwareInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, scl=board.SCL, sda=board.SDA, serial_no=None, channels=None, *args, **kwargs):
        self.i2c = busio.I2C(scl, sda)
        self.am2315 = adafruit_am2320.AM2320(self.i2c)
        self.type = __name__
        super().__init__(serial_no, channels, *args, **kwargs)

    def get_temp(self):
        return self.am2315.temperature

    def get_humidity(self):
        return self.am2315.relative_humidity
