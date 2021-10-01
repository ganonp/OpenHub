from abc import ABC, abstractmethod
from pyhap.accessory import Accessory
from pyhap.accessory import CATEGORY_OTHER
import logging
from OpenHub.globals import id_channels_map \
    , driver
import uuid


class HomeKitSensorInterface(ABC, Accessory):
    logger = logging.getLogger(__name__)
    category = CATEGORY_OTHER
    scale = None
    index = None
    service = None
    char = None

    serial_no = None
    display_name = None

    channel = None

    raw_value_converter = None

    run_debug_message = "Run Debug Message Not Implemented"

    calibrator = None
    aid = None

    def __init__(self, serial_no=uuid.uuid4(), display_name=None, channel_interface_serial_no=None,
                 raw_value_converter=None, *args, **kwargs):
        ABC.__init__(self)
        self.display_name = self.set_display_name(display_name)
        self.serial_no = serial_no
        self.channel_serial_no = channel_interface_serial_no
        self.channel = id_channels_map[str(self.channel_serial_no)]
        Accessory.__init__(self, driver=driver, display_name=self.display_name,
                           *args, **kwargs)
        # super(Bridge, self).__init__(driver=driver, display_name=display_name,
        #                              *args, **kwargs)
        self.service = self.add_functional_service()
        self.char = self.add_functional_service_characteristic()

        # accessories[str(self.serial_no)] = self
        if raw_value_converter is not None:
            self.raw_value_converter = raw_value_converter
            self.raw_value_converter.add_accessory_serial_no(self.serial_no)

    def add_info_service(self):
        serv_info = self.driver.loader.get_service("AccessoryInformation")
        serv_info.configure_char("Name", value=self.display_name)
        serv_info.configure_char("SerialNumber", value=self.serial_no)
        serv_info.configure_char("Manufacturer", value="BellyFrito")
        serv_info.configure_char("Model", value="SoilTemperatureSensor")
        self.add_service(serv_info)

    @abstractmethod
    def set_display_name(self, display_name):
        pass

    @abstractmethod
    def add_functional_service_characteristic(self):
        pass

    @abstractmethod
    def add_functional_service(self):
        pass

    async def run(self):
        data = await self.channel.get_raw_data()
        self.logger.info(self.display_name + " Output: " + str(data))
        if 'averaged' in data.keys():
            if self.scale is None:
                self.char.set_value(float(data['averaged']))
            else:
                self.char.set_value(self.scale*float(data['averaged']))
        elif 'value' in data.keys():
            if self.scale is None:
                self.char.set_value(float(data['value']))
            else:
                self.char.set_value(self.scale * float(data['value']))