from .channel_interface import ChannelInterface
import logging
from OpenHub.globals import id_hardware_map


class VEML7700Lux(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, config, hardware_serial_no=None, serial_no=None, *args, **kwargs):
        self.veml = id_hardware_map[config['hardware']]
        self.serial_no = config['id']
        self.type = config['type']
        super().__init__(hardware_serial_no=hardware_serial_no, serial_no=serial_no, *args, **kwargs)

    async def get_raw_data(self):
        return {'value':self.veml.get_lux()}
