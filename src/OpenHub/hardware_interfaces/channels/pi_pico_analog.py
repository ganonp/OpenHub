import json

from .channel_interface import ChannelInterface
import logging
from OpenHub.globals import id_hardware_map


class PiPicoAnalog(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, config, hardware_serial_no=None, serial_no=None, *args, **kwargs):
        self.pipico = id_hardware_map[config['hardware']]
        self.channel_index = config['channel_index']
        self.serial_no = config['id']
        self.type = config['type']
        super().__init__(hardware_serial_no=self.pipico.serial_no, serial_no=self.serial_no, *args, **kwargs)

    async def get_raw_data(self):
        command = "data"
        channel = str(self.channel_index)
        try:
            response = await self.pipico.send_command(command,channel)
            parsed_response = response.decode('utf-8').replace("'", '"')
            sensor_response = json.loads(parsed_response)
        except Exception as e:
            self.logger.log(level=logging.WARN,msg=str(e))
            return {}
        return sensor_response
