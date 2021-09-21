import json
from OpenHub.hardware_interfaces.channels.channel_interface import ChannelInterface


class ChannelEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ChannelInterface):
            dict = o.__dict__
            dict['type'] = o.__name__

        return json.JSONEncoder.default(self, o)
