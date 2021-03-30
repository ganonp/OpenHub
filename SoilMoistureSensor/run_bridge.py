import logging
import GardenBridge
from pyhap.accessory_driver import AccessoryDriver
import signal
from pyhap.loader import Loader
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

logging.basicConfig(level=logging.DEBUG, format="[%(module)s] %(message)s")


def get_bridge(driver):
    bridge = GardenBridge.GardenBridge(driver)

    return bridge


loader = Loader(path_char="""/home/lesserdaemon/.hap-python/SoilMoistureSensor/characteristics.json""",
                path_service="""/home/lesserdaemon/.hap-python/SoilMoistureSensor/services.json""")
driver = AccessoryDriver(port=51826, persist_file='/home/lesserdaemon/.hap-python/SoilMoistureSensor/accessory.state',
                         loader=loader)
driver.add_accessory(accessory=get_bridge(driver))
signal.signal(signal.SIGTERM, driver.signal_handler)
driver.start()
