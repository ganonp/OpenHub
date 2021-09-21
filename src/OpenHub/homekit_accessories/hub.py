import logging

from pyhap.const import CATEGORY_BRIDGE
from pyhap.accessory import Bridge
from pyhap.accessory import Accessory

from pyhap.const import STANDALONE_AID

from OpenHub.globals import driver

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

    @Accessory.run_at_interval(2)
    async def run(self):
        await super().run()
