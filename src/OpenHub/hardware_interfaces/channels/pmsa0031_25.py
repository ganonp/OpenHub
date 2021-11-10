from .channel_interface import ChannelInterface
import logging


class PMSAAirQuality25(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, pmsa_airquality=None, hardware_serial_no=None, serial_no=None, channel_stats=None,*args, **kwargs):
        self.pmsa_airquality = pmsa_airquality
        self.type = __name__
        super().__init__(config=config,hardware_serial_no=hardware_serial_no, serial_no=serial_no, channel_stats=channel_stats,*args, **kwargs)

    def get_raw_data(self):
        try:
            aqdata = self.pmsa_airquality.read()
            pm25 = aqdata["pm25 standard"]
            return pm25
        except RuntimeError:
            print("Unable to read from sensor, retrying...")
            return -1
