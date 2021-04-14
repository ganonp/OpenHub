import logging
import HardwareInterfaces.DHTInterface as dhti
from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SENSOR


class AirTemperatureHumiditySensor(Accessory):
    logger = logging.getLogger(__name__)
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

    def __init__(self, driver, display_name, **kwargs):
        self.from_json(kwargs["data"])
        if self.display_name is None:
            self.display_name = display_name + "TempAndHumidity"
        super().__init__(driver, self.display_name)
        self.add_air_temp_hum_service()

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

    def add_air_temp_hum_service(self):

        # self.air_temp_hum_service = self.add_preload_service("TemperatureSensor")
        # self.air_temp_hum_service2 = self.add_preload_service("HumiditySensor")
        # self.char_hum = self.air_temp_hum_service.configure_char("CurrentAirHumidity")
        # self.char_temp = self.air_temp_hum_service2.configure_char("CurrentAirTemperature")

        serv_temp = self.add_preload_service('TemperatureSensor')
        serv_humidity = self.add_preload_service('HumiditySensor')

        self.char_temp = serv_temp.get_characteristic('CurrentTemperature')
        self.char_hum = serv_humidity \
            .get_characteristic('CurrentRelativeHumidity')

    async def run(self):
        temperature_f = dhti.get_temp_c()
        humidity = dhti.get_humidity()
        if temperature_f is not None:
            self.char_temp.set_value(temperature_f)
        if humidity is not None:
            self.char_hum.set_value(humidity)
        self.logger.debug("Current Air Temp(F): " + str(temperature_f))
        self.logger.debug("Current Humidity: " + str(humidity))
