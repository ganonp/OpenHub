from SoilMoistureSensor.hardware_interfaces.channels.channel_interface import ChannelInterface
import time
import logging


class DHT22Temp(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, hardware_serial_no=None, serial_no=None, dht_device=None, *args,
                 **kwargs):
        self.type = self.__name__
        self.dhtDevice = dht_device
        super().__init__(hardware_serial_no=hardware_serial_no, serial_no=serial_no, *args, **kwargs)

    def get_raw_data(self):
        try:
            return float(self.dhtDevice.temperature)
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            logger.info(error.args[0])
            time.sleep(2.0)
            self.get_raw_data()
        except Exception as error:
            self.dhtDevice.exit()
            logger.error("DHT Device is down", error)
