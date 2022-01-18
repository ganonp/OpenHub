from .channel_interface import ChannelInterface
import time
import logging
from OpenHub.globals import id_hardware_map


class DHT22Humidity(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, config, hardware_serial_no=None, serial_no=None, dht_device=None,channel_stats=None, *args,
                 **kwargs):
        self.dht = id_hardware_map[config['hardware']]
        self.serial_no = config['id']
        self.type = config['type']

        super().__init__(config=config,hardware_serial_no=self.dht.serial_no, serial_no=self.serial_no, channel_stats=channel_stats,*args, **kwargs)

    async def get_raw_data(self):
        return {'value':float(await self.dht.get_humidity())}
