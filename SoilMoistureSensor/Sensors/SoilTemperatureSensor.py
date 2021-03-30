from pyhap.const import CATEGORY_SENSOR
from pyhap.accessory import Accessory
import logging
import HardwareInterfaces.ModProbeInterface as modProbe


class SoilTemperatureSensor(Accessory):
    logger = logging.getLogger(__name__)
    index = None
    soil_temp_service = None
    char_current_soil_temp = None
    category = CATEGORY_SENSOR
    serial_no = None
    display_name = None

    def __init__(self, driver, display_name, **kwargs):
        self.from_json(kwargs["data"])
        if self.display_name is None:
            self.display_name = display_name + "SoilTemperature"
        super().__init__(driver, self.display_name)
        self.add_soil_temperature_service()

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
        serv_info.configure_char("Model", value="SoilTemperatureSensor")
        self.add_service(serv_info)

    def add_soil_temperature_service(self):

        self.soil_temp_service = self.add_preload_service("TemperatureSensor")
        self.char_current_soil_temp = self.soil_temp_service.configure_char("CurrentTemperature")

    async def run(self):
        self.char_current_soil_temp.set_value(modProbe.read_temp_c())
