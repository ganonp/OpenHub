import json
from OpenHub.hardware_interfaces.channels.stat.max import Max
from OpenHub.hardware_interfaces.channels.stat.min import Min



class StatDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        type = dct['type']
        if type == 'MAX':
            return Max(dct)
        if type == 'MIN':
            return Min(dct)
