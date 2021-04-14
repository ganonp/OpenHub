from pyhap.const import CATEGORY_SENSOR
from pyhap.accessory import Accessory
import logging
import HardwareInterfaces.VEMLInterface as veml


class LightSensor(Accessory):
    logger = logging.getLogger(__name__)
    index = None
    channel = None
    light_service = None
    light_service2 = None
    char_ambient = None
    char_lux = None
    category = CATEGORY_SENSOR
    serial_no = None
    name = None
    display_name = None

    def __init__(self, driver, display_name, **kwargs):
        self.from_json(kwargs["data"])
        if self.display_name is None:
            self.display_name = display_name + "LightSensor"
        super().__init__(driver, self.display_name)
        self.add_light_service()

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
        serv_info.configure_char("Model", value="LightLevelSensor")
        self.add_service(serv_info)

    def add_light_service(self):

        self.light_service = self.add_preload_service("LightSensor")
        self.char_ambient = self.light_service.configure_char("CurrentAmbientLightLevel")


    async def run(self):
        light = veml.veml7700.light
        lux = veml.veml7700.lux
        self.char_ambient.set_value(lux)
        self.logger.debug("Current light: " + str(light))
        self.logger.debug("Current lux: " + str(lux))
