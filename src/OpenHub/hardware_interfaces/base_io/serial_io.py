import logging
from serial import Serial

from hardware_interfaces.base_io.base_io_interface import BaseIOInterface


class SerialIO(BaseIOInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, port, *args, **kwargs):
        self.serial_port = Serial(port.device, 9600, timeout=1)
        super(SerialIO, self).__init__(*args, **kwargs)


