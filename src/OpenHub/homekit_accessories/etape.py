from OpenHub.homekit_accessories.homkit_sensor_interface import HomeKitSensorInterface
import logging

class ETapeSensor(HomeKitSensorInterface):
    logger = logging.getLogger(__name__)
    run_debug_message = "Current ETape Level: "


    def __init__(self, serial_no=None, display_name=None, channel_interface_serial_no=None, *args, **kwargs):
        self.scale = float((1 / 65536) * 100)
        super().__init__(serial_no=serial_no, display_name=display_name,
                         channel_interface_serial_no=channel_interface_serial_no, *args, **kwargs)

    def set_display_name(self, display_name):
        if display_name is None:
            return "ETape"
        else:
            return display_name

    def add_functional_service(self):
        return self.add_preload_service("PressureSensor")

    def add_functional_service_characteristic(self):
        return self.service.get_characteristic('Pressure')

