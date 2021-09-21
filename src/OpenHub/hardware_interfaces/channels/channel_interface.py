from abc import ABC, abstractmethod
import uuid


class ChannelInterface(ABC):

    def __init__(self, hardware_serial_no=None, serial_no=uuid.uuid4(), **kwargs):
        self.serial_no = serial_no
        self.hardware_serial_no = hardware_serial_no
        # hardware_id_channels_map[str(self.serial_no)] = self

    @abstractmethod
    def get_raw_data(self):
        pass
