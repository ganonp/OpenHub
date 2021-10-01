import json
from OpenHub.hardware_interfaces.channels.dht22_humidity import DHT22Humidity
from OpenHub.hardware_interfaces.channels.dht22_temp import DHT22Temp
from OpenHub.hardware_interfaces.channels.mcp3008analog import MCP3008Analog
from OpenHub.hardware_interfaces.channels.mod_probe_temp import ModProbeTemp
from OpenHub.hardware_interfaces.channels.pi_pico_analog import PiPicoAnalog
from OpenHub.hardware_interfaces.channels.pi_pico_ac_analog import PiPicoACAnalog
from OpenHub.hardware_interfaces.channels.pi_pico_pump import PiPicoPump
from OpenHub.hardware_interfaces.channels.veml7700_light import VEML7700Light
from OpenHub.hardware_interfaces.channels.veml7700_lux import VEML7700Lux

from OpenHub.hardware_interfaces.channels.pi_pico_relay import PiPicoRelay


class ChannelDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        type = dct['type']
        if type == DHT22Humidity.__name__:
            return DHT22Humidity(dct)
        if type == DHT22Temp.__name__:
            return DHT22Temp(dct)
        elif type == MCP3008Analog.__name__:
            return MCP3008Analog()

        elif type == ModProbeTemp.__name__:
            return ModProbeTemp(dct)

        elif type == PiPicoAnalog.__name__:
            return PiPicoAnalog(dct)
        elif type == PiPicoACAnalog.__name__:
            return PiPicoACAnalog(dct)
        elif type == PiPicoPump.__name__:
            return PiPicoPump(dct)

        elif type == PiPicoRelay.__name__:
            return PiPicoRelay(dct)

        elif type == VEML7700Light.__name__:
            return VEML7700Light(dct)

        elif type == VEML7700Lux.__name__:
            return VEML7700Lux(dct)
