# import adafruit_dht
import logging
from OpenHub.hardware_interfaces import hardware_interface
from OpenHub.hardware_interfaces.channels.dht22_humidity import DHT22Humidity
from OpenHub.hardware_interfaces.channels.dht22_temp import DHT22Temp


class DHT22(hardware_interface.HardwareInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, pin, serial_no=None, channels=None, *args, **kwargs):
        # self.dhtDevice = adafruit_dht.DHT22(pin)
        self.type = self.__name__
        super().__init__(serial_no, channels, *args, **kwargs)

    def create_channel(self):
        self.create_channel_temp()
        self.create_channel_humidity()

    def create_channel_temp(self):
        self.logger.info('Creating DHT22 Temp Channel: ')
        self.channels["temp"] = DHT22Temp(hardware_serial_no=self.serial_no, dht_device=self.dhtDevice)

    def create_channel_humidity(self):
        self.logger.info('Creating DHT22 Humidity Channel: ')
        self.channels["humidity"] = DHT22Humidity(hardware_serial_no=self.serial_no, dht_device=self.dhtDevice)

    def get_channel(self, channel):
        return self.channels[channel]
    #
    # def get_temp_c(self):
    #     try:
    #         return float(self.dhtDevice.temperature)
    #     except RuntimeError as error:
    #         # Errors happen fairly often, DHT's are hard to read, just keep going
    #         self.logger.info(error.args[0])
    #         time.sleep(2.0)
    #         self.get_temp_c()
    #     except Exception as error:
    #         self.dhtDevice.exit()
    #         self.logger.error("DHT Device is down", error)
    #
    # def get_temp_f(self):
    #     temp_c = self.get_temp_c()
    #     return float(temp_c * (9.0 / 5.0) + 32.0)
    #
    # def get_humidity(self):
    #     try:
    #         return float(self.dhtDevice.humidity)
    #     except RuntimeError as error:
    #         # Errors happen fairly often, DHT's are hard to read, just keep going
    #         self.logger.info(error.args[0])
    #         time.sleep(2.0)
    #         self.get_humidity()
    #     except Exception as error:
    #         self.dhtDevice.exit()
    #         self.logger.error("DHT Device is down", error)
