import logging
import RPi.GPIO as GPIO
import json
from SoilMoistureSensor.hardware_interfaces import mcp3008 as mcpi

from pyhap.const import CATEGORY_SENSOR, CATEGORY_BRIDGE
from pyhap.accessory import Bridge
from pyhap.accessory import Accessory

import SoilMoistureSensor.initializers.hardware.local_setup as local_setup
from SoilMoistureSensor.initializers.hardware import first_time_setup
from pyhap.const import STANDALONE_AID

import os
from SoilMoistureSensor.globals import driver

class Hub(Bridge):
    logger = logging.getLogger(__name__)
    category = CATEGORY_BRIDGE

    def __init__(self, serial_no=None, display_name=None, *args, **kwargs):
        self.serial_no = serial_no
        self.aid = STANDALONE_AID
        Bridge.__init__(self,driver=driver, display_name=display_name,
                         *args, **kwargs)
        self.add_garden_hub_service()

        # driver.add_accessory(self)


    #
    # def __init__(self, driver, **kwargs):
    #     super().__init__(driver, self.display_name)

    def add_info_service(self):
        """Helper method to add the required `AccessoryInformation` service.

        Called in `__init__` to be sure that it is the first service added.
        May be overridden.
        """
        serv_info = self.driver.loader.get_service("AccessoryInformation")
        serv_info.configure_char("Name", value=self.display_name)
        serv_info.configure_char("Manufacturer", value="BellyFrito")
        serv_info.configure_char("Model", value="GardenBridge")
        serv_info.configure_char("SerialNumber", value=self.serial_no)
        self.add_service(serv_info)

    def add_garden_hub_service(self):
        serv_info = self.driver.loader.get_service("OpenHub")
        serv_info.configure_char("IsConfigured", False)

        self.add_service(serv_info)

    @Accessory.run_at_interval(5)
    async def run(self):
        await super().run()
