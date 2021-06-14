import json

from SoilMoistureSensor.hardware_interfaces.channels.channel_interface import ChannelInterface
import logging
from SoilMoistureSensor.globals import id_hardware_map


class PiPicoAnalog(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, config, hardware_serial_no=None, serial_no=None, *args, **kwargs):
        self.pipico = id_hardware_map[config['hardware']]
        self.channel_index = config['channel_index']
        self.serial_no = config['id']
        self.type = config['type']
        super().__init__(hardware_serial_no=self.pipico.serial_no, serial_no=self.serial_no, *args, **kwargs)

    def get_raw_data(self):
        command = "data" + str(self.channel_index)
        try:
            sensor_response = json.loads(self.pipico.send_command(command).decode('utf8').replace("'", '"'))
        except:
            return {}
        return sensor_response
