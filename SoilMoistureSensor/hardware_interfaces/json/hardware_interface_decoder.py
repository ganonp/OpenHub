import json

from SoilMoistureSensor.hardware_interfaces.channels.pi_pico_analog import PiPicoAnalog
from SoilMoistureSensor.hardware_interfaces.dht22 import DHT22
from SoilMoistureSensor.hardware_interfaces.mcp3008 import MCP3008
from SoilMoistureSensor.hardware_interfaces.mod_probe import ModProbe
from SoilMoistureSensor.hardware_interfaces.pi_pico import PiPico
from SoilMoistureSensor.hardware_interfaces.veml_7700 import VEML7700
from SoilMoistureSensor.hardware_interfaces.channels.json.channel_decoder import ChannelDecoder


class HardwareDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        self.channel_decoder = ChannelDecoder()

    def object_hook(self, dct):
        type = dct['type']

        if type == PiPicoAnalog.__name__:
            json.loads(json.dumps(dct), cls=ChannelDecoder)
        else:

            hardware = None
            if type == 'DHT22':
                hardware = DHT22()
            if type == 'MCP3008':
                hardware = MCP3008()
            elif type == 'ModProbe':
                # hardware = ModProbe(dct['base_dir'],dct['base_dir'],dct['id'])
                hardware = ModProbe(serial_no=dct['id'])
            elif type == 'PiPico':
                hardware = PiPico(dct,None)
            elif type == 'VEML7700':
                hardware = VEML7700()
        return hardware
        # hardware.set_channels(channels)
