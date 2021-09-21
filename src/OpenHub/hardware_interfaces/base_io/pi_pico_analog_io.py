import json

from OpenHub.globals import id_hardware_map

from hardware_interfaces.base_io.base_io_interface import BaseIOInterface

import logging


class PiPicoAnalogIO(BaseIOInterface):

    def __init__(self, config, hardware_serial_no=None, serial_no=None, *args, **kwargs):
        self.pipico = id_hardware_map[config['hardware']]
        self.channel_index = config['channel_index']


    async def get_raw_data(self):
        command = "data" + str(self.channel_index)
        try:
            response = await self.pipico.send_command(command)
            parsed_response = response.decode('utf8').replace("'", '"')
            sensor_response = json.loads(parsed_response)
        except Exception as e:
            self.logger.log(level=logging.WARN,msg=str(e))
            return {}
        return sensor_response
