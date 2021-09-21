import digitalio
import logging
import board

from hardware_interfaces.base_io.base_io_interface import BaseIOInterface


class PiDigitalIO(BaseIOInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, cs_pin=board.D5, *args, **kwargs):
        self.cs = digitalio.DigitalInOut(cs_pin)

        super(PiDigitalIO, self).__init__(*args, **kwargs)
