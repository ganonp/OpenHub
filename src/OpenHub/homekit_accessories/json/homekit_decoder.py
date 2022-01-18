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
from OpenHub.homekit_accessories.air_quality import AirQuality

from OpenHub.homekit_accessories.relay import Relay

from OpenHub.data_transformers.constants.constant import Constant
from OpenHub.data_transformers.data_transformer import DataTransformer
from OpenHub.data_transformers.difference import Difference
from OpenHub.data_transformers.divide import Divide
from OpenHub.data_transformers.max import Max
from OpenHub.data_transformers.min import Min
from OpenHub.data_transformers.product import Product
from OpenHub.data_transformers.sum import Sum
from OpenHub.data_transformers.inverse import Inverse

import logging


class HomekitDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        logger = logging.getLogger(HomekitDecoder.__name__)
        logger.info(str(dct))
        type = None
        model = None

        if 'model' in dct.keys():
            model = dct['model']

        if model == 'DataTransformerConstants':
            return Constant(id=dct['id'],index=dct['index'],value=dct['value'])
        elif model == 'DataTransformer':
            type = dct['type']

            if type == 'DIVIDE':
                return Divide(dct)
            if type == 'MAX':
                return Max(dct)
            if type == 'PRODUCT':
                return Product(dct)
            if type == 'DIFFERENCE':
                return Difference(dct)
            if type == 'MIN':
                return Min(dct)
            if type == 'SUM':
                return Sum(dct)
            if type == 'INVERSE':
                return Inverse(dct)
        else:

            if 'type' in dct.keys():
                type = dct['type']

            if type == AirTemperatureSensor.__name__:
                return AirTemperatureSensor(dct['id'], dct['display_name'], dct['channels'][0],config=dct)
            if type == HumiditySensor.__name__:
                return HumiditySensor(dct['id'], dct['display_name'], dct['channels'][0],config=dct)
            elif type == LightSensor.__name__:
                return LightSensor(dct['id'], dct['display_name'], dct['channels'][0],config=dct)

            elif type == SoilMoistureSensor.__name__:
                return SoilMoistureSensor(dct['id'], dct['display_name'], dct['channels'][0],config=dct)

            elif type == SoilTemperatureSensor.__name__:
                return SoilTemperatureSensor(dct['id'], dct['display_name'], dct['channels'][0],config=dct)
            elif type == PressureSensor.__name__:
                return PressureSensor(dct['id'], dct['display_name'], dct['channels'][0],config=dct)
            elif type == Pump.__name__:
                return Pump(dct['id'], dct['display_name'], dct['channels'][0],config=dct)
            elif type == Relay.__name__:
                return Relay(dct['id'], dct['display_name'], dct['channels'][0],config=dct)
            elif type == LiquidLevelSensor.__name__:
                return LiquidLevelSensor(dct['id'], dct['display_name'], dct['channels'][0],config=dct)
            elif type == ETapeSensor.__name__:
                return ETapeSensor(dct['id'], dct['display_name'], dct['channels'][0],config=dct)
            elif type == Camera.__name__:
                return Camera(dct['id'], dct['display_name'])
            elif type == AirQuality.__name__:
                return AirQuality(dct['id'], dct['display_name'], dct['channels'][0],config=dct)
            else:
                return Hub(dct['id'], dct['display_name'])
