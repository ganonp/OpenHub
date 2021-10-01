import logging
from pyhap.const import CATEGORY_SENSOR
from OpenHub.homekit_accessories.homkit_sensor_interface import HomeKitSensorInterface


class HumiditySensor(HomeKitSensorInterface):
    logger = logging.getLogger(__name__)
    run_debug_message = "Current Relative Humidity Level: "


    index = None
    channel = None
    air_temp_hum_service = None
    air_temp_hum_service2 = None
    char_temp = None
    char_hum = None
    category = CATEGORY_SENSOR
    serial_no = None
    name = None
    display_name = None

    def __init__(self, serial_no=None, display_name=None, channel_interface_serial_no=None, *args, **kwargs):
        super().__init__(serial_no=serial_no, display_name=display_name,
                         channel_interface_serial_no=channel_interface_serial_no, *args, **kwargs)

    def set_display_name(self, display_name):
        if display_name is None:
            return "Humidity Sensor"
        else:
            return display_name

    def as_json(self):
        sensor_dict = {"aid": self.aid, "serial_no": self.serial_no,

                       "display_name": self.display_name}
        return sensor_dict

    def from_json(self, data):
        if "serial_no" in data.keys():
            self.serial_no = data["serial_no"]
        if "index" in data.keys():
            self.index = data["index"]
        if "name" in data.keys():
            self.name = data["name"]
        if "aid" in data.keys():
            self.aid = data["aid"]
        if "display_name" in data.keys():
            self.display_name = data["display_name"]

    def add_info_service(self):

        serv_info = self.driver.loader.get_service("AccessoryInformation")
        serv_info.configure_char("Name", value=self.display_name)
        serv_info.configure_char("SerialNumber", value=self.serial_no)
        serv_info.configure_char("Manufacturer", value="BellyFrito")
        serv_info.configure_char("Model", value="AirTempAndHumiditySensor")
        self.add_service(serv_info)

    def add_functional_service(self):
        return self.add_preload_service("HumiditySensor")

    def add_functional_service_characteristic(self):
        return self.service.get_characteristic('CurrentRelativeHumidity')
    #
    # async def run(self):
    #     temperature_f = dhti.get_temp_c()
    #     humidity = dhti.get_humidity()
    #     if temperature_f is not None:
    #         self.char_temp.set_value(temperature_f)
    #     if humidity is not None:
    #         self.char_hum.set_value(humidity)
    #     self.logger.debug("Current Air Temp(F): " + str(temperature_f))
    #     self.logger.debug("Current Humidity: " + str(humidity))
