import logging
from OpenHub.homekit_accessories.homkit_sensor_interface import HomeKitSensorInterface


class AirTemperatureSensor(HomeKitSensorInterface):
    logger = logging.getLogger(__name__)
    run_debug_message = "Current Air Temperature: "

    def __init__(self, serial_no=None, display_name=None, channel_interface_serial_no=None, *args, **kwargs):
        super().__init__(serial_no=serial_no, display_name=display_name,
                         channel_interface_serial_no=channel_interface_serial_no, *args, **kwargs)

    def set_display_name(self, display_name):
        if display_name is None:
            return display_name + "Air Temperature"
        else:
            return display_name

    def add_functional_service(self):
        return self.add_preload_service('TemperatureSensor')

    def add_functional_service_characteristic(self):
        return self.service.get_characteristic('CurrentTemperature')
    #
    # async def run(self):
    #
    #     temperature_f = dhti.get_temp_c()
    #     humidity = dhti.get_humidity()
    #     if temperature_f is not None:
    #         self.char_temp.set_value(temperature_f)
    #     if humidity is not None:
    #         self.char_hum.set_value(humidity)
    #
