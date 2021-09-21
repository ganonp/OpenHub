from .channel_interface import ChannelInterface
import logging


class ModProbeTemp(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, device_file, hardware_serial_no=None, serial_no=None, *args, **kwargs):
        self.device_file = device_file
        self.type = self.__name__
        super().__init__(hardware_serial_no=hardware_serial_no, serial_no=serial_no, *args, **kwargs)

    def get_raw_data(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
