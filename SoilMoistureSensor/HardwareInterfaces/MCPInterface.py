import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import logging

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

analogInputs = {}
logger = logging.getLogger(__name__)


def get_voltage_for_channel(channel_index):
    logger.debug("Channel: " + str(channel_index))
    return analogInputs[channel_index].voltage


def setup(num_channels):
    for index in range(num_channels):
        analogInputs[index] = AnalogIn(mcp, int(index))
