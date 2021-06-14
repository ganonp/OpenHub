import json
from SoilMoistureSensor.hardware_interfaces.channels.dht22_humidity import DHT22Humidity
from SoilMoistureSensor.hardware_interfaces.channels.dht22_temp import DHT22Temp
from SoilMoistureSensor.hardware_interfaces.channels.mcp3008analog import MCP3008Analog
from SoilMoistureSensor.hardware_interfaces.channels.mod_probe_temp import ModProbeTemp
from SoilMoistureSensor.hardware_interfaces.channels.pi_pico_analog import PiPicoAnalog
from SoilMoistureSensor.hardware_interfaces.channels.pi_pico_pump import PiPicoPump
from SoilMoistureSensor.hardware_interfaces.channels.veml7700_light import VEML7700Light
from SoilMoistureSensor.hardware_interfaces.channels.veml7700_lux import VEML7700Lux

class ChannelDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        type = dct['type']
        if type == DHT22Humidity.__name__:
            return DHT22Humidity()
        if type == DHT22Temp.__name__:
            return DHT22Temp()
        elif type == MCP3008Analog.__name__:
            return MCP3008Analog()

        elif type == ModProbeTemp.__name__:
            return ModProbeTemp()

        elif type == PiPicoAnalog.__name__:
            return PiPicoAnalog(dct)

        elif type == PiPicoPump.__name__:
            return PiPicoPump(dct)

        elif type == VEML7700Light.__name__:
            return VEML7700Light()

        elif type == VEML7700Lux.__name__:
            return VEML7700Lux()
