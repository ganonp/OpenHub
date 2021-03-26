import logging
import GardenBridge
from pyhap.accessory_driver import AccessoryDriver
import signal

logging.basicConfig(level=logging.DEBUG, format="[%(module)s] %(message)s")
logger = logging.getLogger(__name__)


def calibrate():
    driver = AccessoryDriver(port=51826,
                             persist_file='/home/lesserdaemon/.hap-python/SoilMoistureSensor/accessory.state')
    signal.signal(signal.SIGTERM, driver.signal_handler)
    bridge = GardenBridge.GardenBridge(driver, 'Bridge')
    logger.info("Setting up new config")
    bridge.configure_first_time()
    channel = input("Which channel would you like to calibrate?")
    bridge.calibrate_sensor(channel)
    bridge.update_config_sensors()


calibrate()
