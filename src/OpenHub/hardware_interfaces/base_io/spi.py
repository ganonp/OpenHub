import logging
import board
import busio

from hardware_interfaces.base_io.base_io_interface import BaseIOInterface


class SPI(BaseIOInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, sck=board.SCK, miso=board.MISO, mosi=board.MOSI, *args, **kwargs):
        self.spi = busio.SPI(clock=sck, MISO=miso, MOSI=mosi)
        super(SPI, self).__init__(*args, **kwargs)
