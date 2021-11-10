from abc import ABC, abstractmethod
from pyhap.accessory import Accessory
from pyhap.accessory import CATEGORY_OTHER
import logging
from OpenHub.globals import id_channels_map \
    , driver, accessory_id_data_transformer_map
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

    data_transformer = None

    def __init__(self, serial_no=uuid.uuid4(), display_name=None, channel_interface_serial_no=None,
                 data_transformer=None,config=None, *args, **kwargs):
        ABC.__init__(self)
        self.display_name = self.set_display_name(display_name)
        self.serial_no = serial_no
        self.channel_serial_no = channel_interface_serial_no
        self.channel = id_channels_map[str(self.channel_serial_no)]
        Accessory.__init__(self, driver=driver, display_name=self.display_name,
                           *args, **kwargs)

        self.service = self.add_functional_service()
        self.char = self.add_functional_service_characteristic()
        if config is not None and 'datatransformer' in config.keys():
            self.data_transformer = config['datatransformer']
        if config is not None and 'data_transformer' in config.keys():
            self.data_transformer = config['data_transformer']


    def add_info_service(self):
        serv_info = self.driver.loader.get_service("AccessoryInformation")
        serv_info.configure_char("Name", value=self.display_name)
        serv_info.configure_char("SerialNumber", value=self.serial_no)
        serv_info.configure_char("Manufacturer", value="BellyFrito")
        serv_info.configure_char("Model", value="DEFAULT")
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
        if self.data_transformer is None:
            data = await self.channel.run()
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
        else:
            val = await self.data_transformer.run()
            self.logger.info(self.display_name + " Output: " + str(val))

            self.char.set_value(float(val))