from .channel_interface import ChannelInterface
import logging
from OpenHub.globals import id_hardware_map
import asyncio

class AM2315Temperature(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, config, hardware_serial_no=None, serial_no=None, channel_stats=None,*args, **kwargs):
        self.am2315 = id_hardware_map[config['hardware']]
        self.serial_no = config['id']
        self.type = config['type']
        super().__init__(config=config,hardware_serial_no=hardware_serial_no, serial_no=self.serial_no, channel_stats=channel_stats,*args, **kwargs)


    async def get_raw_data(self):
        temperature = None
        while temperature is None:
            try:
                temperature = self.am2315.get_temp()
            except Exception as e:
                self.logger.info(str(e))
                await asyncio.sleep(0.01)


        return {'value':temperature}