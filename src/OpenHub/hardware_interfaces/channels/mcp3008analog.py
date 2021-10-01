from adafruit_mcp3xxx.analog_in import AnalogIn
from .channel_interface import ChannelInterface
import logging
import uuid
from OpenHub.globals import id_hardware_map


class MCP3008Analog(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, mcp=None, channel_index=None, hardware_serial_no=None, serial_no=uuid.uuid4(),
                 *args, **kwargs):
        super.__init__(hardware_serial_no)
        self.type = __name__
        self.analog_in = AnalogIn(mcp, channel_index)
        super().__init__(hardware_serial_no=hardware_serial_no, serial_no=serial_no, *args, **kwargs)

    def get_raw_data(self):
        return self.analog_in.voltage
