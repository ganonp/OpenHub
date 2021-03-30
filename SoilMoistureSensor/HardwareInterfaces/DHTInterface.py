import adafruit_dht
import board
import time
import logging

dhtDevice = adafruit_dht.DHT22(board.D17)
logger = logging.getLogger(__name__)


def get_temp_c():
    try:
        return float(dhtDevice.temperature)
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        logger.info(error.args[0])
        time.sleep(2.0)
        get_temp_c()
    except Exception as error:
        dhtDevice.exit()
        logger.error("DHT Device is down", error)


def get_temp_f():
    temp_c = get_temp_c()
    return float(temp_c * (9.0 / 5.0) + 32.0)


def get_humidity():
    try:
        return float(dhtDevice.humidity)
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        logger.info(error.args[0])
        time.sleep(2.0)
        get_humidity()
    except Exception as error:
        dhtDevice.exit()
        logger.error("DHT Device is down", error)
