import logging
from OpenHub.hardware_interfaces import hardware_interface
from OpenHub.hardware_interfaces.channels.dht22_humidity import DHT22Humidity
from OpenHub.hardware_interfaces.channels.dht22_temp import DHT22Temp
import time
from pigpio_dht import DHT22 as dht_22


class DHT22(hardware_interface.HardwareInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, pin_no=18, serial_no=None, channels=None, *args, **kwargs):
        self.dhtDevice = dht_22(pin_no)
        self.type = __name__
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

    def get_data(self, type):
        valid = False
        while valid is False:
            data = self.dhtDevice.read()
            valid = data['valid']
        return data[type]

    def get_temp_c(self):
        return self.get_data('temp_c')

    def get_temp_f(self):
        return self.get_data('temp_f')

    def get_humidity(self):
        return self.get_data('humidity')
