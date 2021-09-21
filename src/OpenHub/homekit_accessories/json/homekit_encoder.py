import json
from OpenHub.hardware_interfaces.channels.json.channel_encoder import ChannelEncoder

from OpenHub.hardware_interfaces.channels.channel_interface import ChannelInterface


class HomekitEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ChannelInterface):
            dict = o.__dict__
            dict['type'] = o.__name__
            dict['channel'] = json.dump(o.channel, cls= ChannelEncoder)
            #
            # if isinstance(o, DHT22Humidity):
            #     dict['type'] = 'DHT22Humidity'
            #     return dict
            # elif isinstance(o, DHT22Temp):
            #     return {}
            #
            # elif isinstance(o, MCP3008Analog):
            #     return {}
            #
            # elif isinstance(o, ModProbeTemp):
            #     return {}
            #
            # elif isinstance(o, PiPicoAnalog):
            #     return {}
            #
            # elif isinstance(o, PiPicoPump):
            #     return {}
            #
            # elif isinstance(o, VEML7700Light):
            #     return {}
            #
            # elif isinstance(o, VEML7700Lux):
            #     return {}

        return json.JSONEncoder.default(self, o)
