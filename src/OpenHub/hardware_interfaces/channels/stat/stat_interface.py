from abc import ABC, abstractmethod
import uuid
from OpenHub.globals import id_stats_map
import logging
class StatInterface(ABC):
    logger = logging.getLogger(__name__)
    def __init__(self, dct, id=None, value=None,type=None,channel_serial=None,*args, **kwargs):
        if dct is not None:
            if 'id' in dct:
                self.id = dct['id']
            else:
                self.id = str(uuid.uuid4())
            if 'value' in dct:
                self.old_value = dct['value']
                self.value = dct['value']
            if 'channel' in dct:
                self.channel_serial = dct['channel']
            if 'type' in dct:
                self.type = dct['type']
        else:
            self.id = id
            self.value = value
            self.old_value = value
            self.type = type
            self.channel_serial = channel_serial
        self.update_on_server = False
        self.logger.info('added to id stats map')
        self.logger.info(str(id_stats_map))
        id_stats_map[str(self.id)] = self
        super().__init__(*args,**kwargs)


    @abstractmethod
    def update(self, value):
        pass

    def check_if_value_updated(self):
        if self.old_value != self.value:
            self.update_on_server = True

    def value_updated_on_server(self):
        self.old_value = self.value
        self.update_on_server = False;