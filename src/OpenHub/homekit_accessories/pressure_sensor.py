from OpenHub.homekit_accessories.homkit_sensor_interface import HomeKitSensorInterface
import logging


class PressureSensor(HomeKitSensorInterface):
    logger = logging.getLogger(__name__)
    run_debug_message = "Current Pressure: "

    def __init__(self, serial_no=None, display_name=None, channel_interface_serial_no=None, *args, **kwargs):
        self.scale = float((1.2*145.038) /(3.234*65536))
        super().__init__(serial_no=serial_no, display_name=display_name,
                         channel_interface_serial_no=channel_interface_serial_no, *args, **kwargs)

    def set_display_name(self, display_name):
        if display_name is None:
            return "Pressure Sensor"
        else:
            return display_name

    def add_functional_service(self):
        return self.add_preload_service("PressureSensor")

    def add_functional_service_characteristic(self):
        return self.service.get_characteristic('Pressure')
