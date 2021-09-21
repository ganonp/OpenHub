import logging
from abc import ABC
import json


class RawValueConverter(ABC):
    logger = logging.getLogger(__name__)

    calibration_directory = None
    homekit_accessory_serial_no = None

    def __init__(self):
        super().__init__()

    def add_accessory_serial_no(self, serial_no):
        if self.homekit_accessory_serial_no is None:
            self.homekit_accessory_serial_no = serial_no
