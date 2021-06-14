from pyhap.accessory_driver import AccessoryDriver
from pyhap.loader import Loader
# import garden_bridge
from config_files import HAP_PYTHON_CHARACTERISTICS_FILE, HAP_PYTHON_SERVICES_FILE, HAP_PYTHON_ACCESSORIES_FILE

accessories = {}
id_hardware_map = {}
picos = []
hardware_id_channels_map = {}
id_channels_map = {}
calibration = {}
hub = None

#
# def get_bridge(driver):
#     bridge = garden_bridge.GardenBridge(driver)
#     return bridge
#
#
loader = Loader(path_char=HAP_PYTHON_CHARACTERISTICS_FILE,
                path_service=HAP_PYTHON_SERVICES_FILE)

driver = AccessoryDriver(port=51826, persist_file=HAP_PYTHON_ACCESSORIES_FILE,
                         loader=loader)
# driver.add_accessory(accessory=get_bridge(driver))
