import json
from calibrators.soil_moisture_voltage_converter import SoilMoistureVoltageConverter
from calibrators import RawValueConverter


class RawValueDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        type = dct['type']

        if type == SoilMoistureVoltageConverter.__name__:
            return SoilMoistureVoltageConverter(soil_moisture_sensor_serial_no=dct['soil_moisture_sensor_serial_no'],
                                                m=dct['m'], b=dct['b'], max_voltage=dct['max_voltage'],
                                                min_voltage=dct['min_voltage'])
        else:
            return RawValueConverter()
