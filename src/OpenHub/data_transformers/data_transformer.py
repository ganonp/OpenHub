import logging
from abc import ABC, abstractmethod
import json
from globals import id_channels_map,id_stats_map

class DataTransformer(ABC):
    logger = logging.getLogger(__name__)

    homekit_accessory_serial_no = None

    def __init__(self, dct, data_transformers=None):
        self.channels = []
        self.stats=[]
        for channel in dct['channels']:
            self.channels.append(id_channels_map[channel])
        for stat in dct['stats']:
            self.stats.append(id_stats_map[str(stat['id'])])
        self.data_transformers = data_transformers

        super().__init__()

    async def run(self):
        outputs = []
        if self.data_transformers is not None:
            for transformer in self.data_transformers:
                outputs.append(await transformer.run())
        if self.channels is not None:
            for channel in self.channels:
                outputs.append(await channel.run())
        if self.stats is not None:
            for stat in self.stats:
                outputs.append(stat.value)

        return self.perform_op(outputs)

    @abstractmethod
    def perform_op(self, inputs):
        pass
