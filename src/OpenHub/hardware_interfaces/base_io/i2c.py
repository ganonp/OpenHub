import logging
import board
import busio

from hardware_interfaces.base_io.base_io_interface import BaseIOInterface


class I2C(BaseIOInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, scl=board.SCL, sda=board.SDA, *args, **kwargs):
        self.i2c = busio.I2C(scl, sda)
        super(I2C, self).__init__(*args, **kwargs)
