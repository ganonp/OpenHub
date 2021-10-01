from .channel_interface import ChannelInterface
import logging
from OpenHub.globals import id_hardware_map
import time

class ModProbeTemp(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, config, hardware_serial_no=None, serial_no=None, *args, **kwargs):
        self.mod_probe = id_hardware_map[config['hardware']]
        self.serial_no = config['id']
        self.type = config['type']
        self.device_file = self.mod_probe.device_file
        super().__init__(hardware_serial_no=self.mod_probe.serial_no, serial_no=self.serial_no, *args, **kwargs)

    async def get_raw_data(self):
        return {'value':self.mod_probe.read_temp_c()}
