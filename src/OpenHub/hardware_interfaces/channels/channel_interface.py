from abc import ABC, abstractmethod
import uuid
from .stats.stats import Stats
from OpenHub.hardware_interfaces.channels.stat.max import Max
from OpenHub.hardware_interfaces.channels.stat.min import Min

class ChannelInterface(ABC):
    def __init__(self, config, hardware_serial_no=None, serial_no=uuid.uuid4(), channel_stats=None, **kwargs):
        self.serial_no = serial_no
        self.hardware_serial_no = hardware_serial_no

        if 'keep_statistics' in config:
            self.keep_statistics = config['keep_statistics']
        else:
            self.keep_statistics = False

        if self.keep_statistics:
            if channel_stats is not None and len(channel_stats)>0:
                self.stats = Stats(channel_stats)
            else:
                min = Min(id=str(uuid.uuid4()),value=float('inf'),channel_serial=self.serial_no)
                max = Max(id=str(uuid.uuid4()),value=float('-inf'),channel_serial=self.serial_no)
                self.stats = Stats([min,max])

    def update_stats(self,value):
        if self.keep_statistics:
            self.stats.update(value)
            self.stats.update_on_server()

    async def run(self):
        value = await self.get_raw_data()
        if self.keep_statistics:
            if 'averaged' in value.keys():
                self.update_stats(value['averaged'])
            elif 'value' in value.keys():
                self.update_stats(value['value'])
            else:
                self.update_stats(value)
        return value


    @abstractmethod
    async def get_raw_data(self):
        pass
