import logging

from hardware_interfaces.base_io.base_io_interface import BaseIOInterface


class PiPicoGPI(BaseIOInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, pin=1, *args, **kwargs):
        self.pin = pin
        super(PiPicoGPI, self).__init__(*args, **kwargs)
