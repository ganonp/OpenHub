import logging
import DHTInterface as dhti
from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SENSOR


class AirTemperatureHumiditySensor(Accessory):
    logger = logging.getLogger(__name__)
    index = None
    channel = None
    air_temp_hum_service = None
    char_temp = None
    char_hum = None
    category = CATEGORY_SENSOR
    serial_no = None
    name = None
    display_name = None

    def __init__(self, driver, **kwargs):
        self.from_json(kwargs["data"])
        super().__init__(driver, self.display_name)
        self.add_air_temp_hum_service()

    def as_json(self):
        sensor_dict = {"name": self.name, "index": self.index, "aid": self.aid, "serial_no": self.serial_no,

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

    def add_air_temp_hum_service(self):

        self.air_temp_hum_service = self.add_preload_service("AirTempAndHumiditySensor")
        self.char_hum = self.air_temp_hum_service.configure_char("CurrentAirHumidity")
        self.char_temp = self.air_temp_hum_service.configure_char("CurrentAirTemperature")

    async def run(self):
        temperature_f = dhti.get_temp_f()
        humidity = dhti.get_humidity()
        self.char_temp.set_value(temperature_f)
        self.char_hum.set_value(temperature_f)
        self.logger.debug("Current Air Temp(F): " + str(temperature_f))
        self.logger.debug("Current Humidity: " + str(humidity))
