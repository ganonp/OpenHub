import json
from SoilMoistureSensor.homekit_accessories.air_temperature import AirTemperatureSensor
from SoilMoistureSensor.homekit_accessories.hub import Hub
from SoilMoistureSensor.homekit_accessories.humidity import HumiditySensor
from SoilMoistureSensor.homekit_accessories.light_sensor import LightSensor
from SoilMoistureSensor.homekit_accessories.soil_moisture_sensor import SoilMoistureSensor
from SoilMoistureSensor.homekit_accessories.soil_temperature_sensor import SoilTemperatureSensor
from SoilMoistureSensor.homekit_accessories.pressure_sensor import PressureSensor
from SoilMoistureSensor.homekit_accessories.liquid_level_sensor import LiquidLevelSensor
from SoilMoistureSensor.homekit_accessories.etape import ETapeSensor
from SoilMoistureSensor.homekit_accessories.pump import Pump

class HomekitDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        type = dct['type']

        if type == AirTemperatureSensor.__name__:
            return AirTemperatureSensor()
        if type == HumiditySensor.__name__:
            return HumiditySensor()
        elif type == LightSensor.__name__:
            return LightSensor()

        elif type == SoilMoistureSensor.__name__:
            return SoilMoistureSensor()

        elif type == SoilTemperatureSensor.__name__:
            return SoilTemperatureSensor()
        elif type == PressureSensor.__name__:
            return PressureSensor(dct['id'],dct['display_name'],dct['channels'][0])
        elif type == Pump.__name__:
            return Pump(dct['id'],dct['display_name'],dct['channels'][0])
        elif type == LiquidLevelSensor.__name__:
            return LiquidLevelSensor(dct['id'],dct['display_name'],dct['channels'][0])
        elif type == ETapeSensor.__name__:
            return ETapeSensor(dct['id'],dct['display_name'],dct['channels'][0])
        else:
            return Hub(dct['id'],dct['display_name'])
