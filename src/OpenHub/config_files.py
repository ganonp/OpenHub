import os

HOME_DIRECTORY = '/openhub/'
SRC_DIRECTORY = HOME_DIRECTORY + 'src/'
CONFIG = HOME_DIRECTORY + 'config/'
HARDWARE_CONFIG_FILE = CONFIG + 'hardware/config.txt'
HOMEKIT_CONFIG_FILE = CONFIG + 'homekit_accessories/config.txt'
CALIBRATION_CONFIG_FILE = CONFIG + 'calibration/config.txt'


# HAP_PYTHON_CHARACTERISTICS_FILE="""/home/lesserdaemon/.hap-python/OpenHub/characteristics.json"""
HAP_PYTHON_CHARACTERISTICS_FILE=os.path.dirname(__file__) + """/characteristics.json"""
# HAP_PYTHON_SERVICES_FILE="""/home/lesserdaemon/.hap-python/OpenHub/services.json"""
HAP_PYTHON_SERVICES_FILE=os.path.dirname(__file__)+"""/services.json"""


HAP_PYTHON_ACCESSORIES_FILE="""~/accessory.state"""
# HAP_PYTHON_ACCESSORIES_FILE='/home/lesserdaemon/.hap-python/OpenHub/accessory.state'

# HARDWARE_CONFIG_FILE_OLD="""/home/lesserdaemon/.hap-python/OpenHub/soil_sensor.json"""