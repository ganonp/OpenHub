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
loader = None
driver = None
#
# def get_bridge(driver):
#     bridge = garden_bridge.GardenBridge(driver)
#     return bridge
#
#

# driver.add_accessory(accessory=get_bridge(driver))
