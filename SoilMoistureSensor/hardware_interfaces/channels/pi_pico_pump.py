from SoilMoistureSensor.hardware_interfaces.channels.channel_interface import ChannelInterface
import logging
from SoilMoistureSensor.globals import id_hardware_map


class PiPicoPump(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, config, hardware_serial_no=None, serial_no=None, *args, **kwargs):
        self.pipico = id_hardware_map[config['hardware']]
        self.channel_index = config['channel_index']
        self.serial_no = config['id']
        self.type = config['type']
        super().__init__(hardware_serial_no=self.pipico.serial_no, serial_no=self.serial_no, *args, **kwargs)


    def get_raw_data(self):
        # command = "stat" + str(self.channel_index) + "\n"
        command = "init" + "\n"
        return self.pipico.send_command(command)

    def turn_on(self):
        command = "stat" + str(self.channel_index) + "on\n"
        return self.pipico.send_command(command)

    def turn_off(self):
        command = "stat" + str(self.channel_index) + "off\n"
        return self.pipico.send_command(command)
