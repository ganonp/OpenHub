import logging
from OpenHub.homekit_accessories.homkit_sensor_interface import HomeKitSensorInterface


class AirQuality(HomeKitSensorInterface):
    logger = logging.getLogger(__name__)
    run_debug_message = "Current Air Quality: "

    def __init__(self, serial_no=None, display_name=None, channel_interface_serial_no=None, *args, **kwargs):
        super().__init__(serial_no=serial_no, display_name=display_name,
                         channel_interface_serial_no=channel_interface_serial_no, *args, **kwargs)

    def set_display_name(self, display_name):
        if display_name is None:
            return "Air Quality"
        else:
            return display_name

    def add_functional_service(self):
        return self.add_preload_service('AirQualitySensor')

    def add_additional_services(self):
        self.pm25 = self.add_preload_service('PM2.5Density')
        self.pm100 = self.add_preload_service('PM10Density')

    def add_functional_service_characteristic(self):
        return self.service.get_characteristic('AirQuality')

    async def run(self):
        data = await self.channel.get_raw_data()
        self.logger.info(self.display_name + " Output: " + str(data))
        self.char.set_value(3)
        self.pm25.set_value(data)

