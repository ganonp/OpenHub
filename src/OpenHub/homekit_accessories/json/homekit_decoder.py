import json
from OpenHub.homekit_accessories.air_temperature import AirTemperatureSensor
from OpenHub.homekit_accessories.hub import Hub
from OpenHub.homekit_accessories.humidity import HumiditySensor
from OpenHub.homekit_accessories.light_sensor import LightSensor
from OpenHub.homekit_accessories.soil_moisture_sensor import SoilMoistureSensor
from OpenHub.homekit_accessories.soil_temperature_sensor import SoilTemperatureSensor
from OpenHub.homekit_accessories.pressure_sensor import PressureSensor
from OpenHub.homekit_accessories.liquid_level_sensor import LiquidLevelSensor
from OpenHub.homekit_accessories.etape import ETapeSensor
from OpenHub.homekit_accessories.pump import Pump
from OpenHub.homekit_accessories.camera import Camera

from OpenHub.homekit_accessories.relay import Relay


class HomekitDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        type = dct['type']

        if type == AirTemperatureSensor.__name__:
            return AirTemperatureSensor(dct['id'],dct['display_name'],dct['channels'][0])
        if type == HumiditySensor.__name__:
            return HumiditySensor(dct['id'],dct['display_name'],dct['channels'][0])
        elif type == LightSensor.__name__:
            return LightSensor(dct['id'],dct['display_name'],dct['channels'][0])

        elif type == SoilMoistureSensor.__name__:
            return SoilMoistureSensor(dct['id'],dct['display_name'],dct['channels'][0])

        elif type == SoilTemperatureSensor.__name__:
            return SoilTemperatureSensor(dct['id'],dct['display_name'],dct['channels'][0])
        elif type == PressureSensor.__name__:
            return PressureSensor(dct['id'],dct['display_name'],dct['channels'][0])
        elif type == Pump.__name__:
            return Pump(dct['id'],dct['display_name'],dct['channels'][0])
        elif type == Relay.__name__:
            return Relay(dct['id'],dct['display_name'],dct['channels'][0])
        elif type == LiquidLevelSensor.__name__:
            return LiquidLevelSensor(dct['id'],dct['display_name'],dct['channels'][0])
        elif type == ETapeSensor.__name__:
            return ETapeSensor(dct['id'],dct['display_name'],dct['channels'][0])
        elif type == Camera.__name__:
            return Camera(dct['id'],dct['display_name'])
        else:
            return Hub(dct['id'],dct['display_name'])
