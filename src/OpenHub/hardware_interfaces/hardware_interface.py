from abc import ABC, abstractmethod
import uuid
from OpenHub.globals import id_hardware_map


class HardwareInterface(ABC):

    def __init__(self, serial_no=uuid.uuid4(), *args, **kwargs):
        self.serial_no = serial_no

        id_hardware_map[str(self.serial_no)] = self



