from .channel_interface import ChannelInterface
import logging
from OpenHub.globals import id_hardware_map


class PMSA0031100(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self,config, pmsa_airquality=None, hardware_serial_no=None, serial_no=None, channel_stats=None,*args, **kwargs):
        self.pmsa_airquality = id_hardware_map[config['hardware']]
        self.serial_no = config['id']
        self.type = __name__
        super().__init__(config=config,hardware_serial_no=self.pmsa_airquality.serial_no, serial_no=self.serial_no, channel_stats=channel_stats,*args, **kwargs)

    async def get_raw_data(self):
        try:
            aqdata = self.pmsa_airquality.pm25.read()
            pm25 = aqdata["pm100 standard"]
            return {'value': float(pm25)}
        except RuntimeError:
            print("Unable to read from sensor, retrying...")
            return float(1)