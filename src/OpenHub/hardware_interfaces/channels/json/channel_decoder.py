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
from OpenHub.hardware_interfaces.channels.am2315_temperature import AM2315Temperature
from OpenHub.hardware_interfaces.channels.am2315_humidity import AM2315Humidity
from OpenHub.hardware_interfaces.channels.pmsa0031_25 import PMSA003125
from OpenHub.hardware_interfaces.channels.pmsa0031_100 import PMSA0031100
# from OpenHub.hardware_interfaces.channels.pmsa0031 import PMSA0031

from OpenHub.hardware_interfaces.channels.pi_pico_relay import PiPicoRelay
from OpenHub.hardware_interfaces.channels.pi_relay import PiRelay
from OpenHub.hardware_interfaces.channels.stat.max import Max
from OpenHub.hardware_interfaces.channels.stat.min import Min
import logging

class ChannelDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, config):
        logger = logging.getLogger(ChannelDecoder.__name__)
        logger.info(str(config))
        model = config['model']
        type = config['type']
        if model=='ChannelStats' or model=='ChannelStat':
            if type == 'MAX':
                return Max(config)
            if type == 'MIN':
                return Min(config)

        type = config['type']
        if 'channelstats_set' in config.keys():
            stats=config['channelstats_set']
        elif 'channel_stats' in config.keys():
            stats=config['channelstats']
        else:
            stats=None

        if type == DHT22Humidity.__name__:
            return DHT22Humidity(config=config, channel_stats=stats)
        if type == DHT22Temp.__name__:
            return DHT22Temp(config=config, channel_stats=stats)
        elif type == MCP3008Analog.__name__:
            return MCP3008Analog()

        elif type == ModProbeTemp.__name__:
            return ModProbeTemp(config=config, channel_stats=stats)

        elif type == PiPicoAnalog.__name__:
            return PiPicoAnalog(config=config, channel_stats=stats)
        elif type == PiPicoACAnalog.__name__:
            return PiPicoACAnalog(config=config, channel_stats=stats)
        elif type == PiPicoPump.__name__:
            return PiPicoPump(config=config, channel_stats=stats)

        elif type == PiPicoRelay.__name__:
            return PiPicoRelay(config=config, channel_stats=stats)
        elif type == PiRelay.__name__:
            return PiRelay(config=config, channel_stats=stats)
        elif type == VEML7700Light.__name__:
            return VEML7700Light(config=config, channel_stats=stats)

        elif type == VEML7700Lux.__name__:
            return VEML7700Lux(config=config, channel_stats=stats)
        elif type == AM2315Temperature.__name__:
            return AM2315Temperature(config=config, channel_stats=stats)
        elif type == AM2315Humidity.__name__:
            return AM2315Humidity(config=config, channel_stats=stats)
        elif type == PMSA003125.__name__:
            return PMSA003125(config=config, channel_stats=stats)
        elif type == PMSA0031100.__name__:
            return PMSA0031100(config=config, channel_stats=stats)

        return super().object_hook( config)