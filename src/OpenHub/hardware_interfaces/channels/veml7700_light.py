from .channel_interface import ChannelInterface
import logging


class VEML7700Light(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, veml=None, hardware_serial_no=None, serial_no=None, *args, **kwargs):
        self.veml = veml
        self.type = self.__name__
        super().__init__(hardware_serial_no=hardware_serial_no, serial_no=serial_no, *args, **kwargs)

    def get_raw_data(self):
        return self.veml.veml7700.light
