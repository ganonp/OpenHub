import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import logging
from OpenHub.hardware_interfaces import hardware_interface
from OpenHub.hardware_interfaces.channels.mcp3008analog import MCP3008Analog


class MCP3008(hardware_interface.HardwareInterface):
    logger = logging.getLogger(__name__)
    channels = []

    def __init__(self, num_channels=3, sck=board.SCK, miso=board.MISO, mosi=board.MOSI, cs_pin=board.D5, serial_no=None,
                 channels=None, *args, **kwargs):
        self.spi = busio.SPI(clock=sck, MISO=miso, MOSI=mosi)
        self.cs = digitalio.DigitalInOut(cs_pin)
        self.mcp = MCP.MCP3008(self.spi, self.cs)
        self.num_channels = num_channels
        self.type = __name__

        super().__init__(serial_no, channels, *args, **kwargs)

    def create_channel(self):
        pin = str(input("Which channel is this (0-8)?"))
        return self.create_analog_channel(pin)

    def create_analog_channel(self, channel_index):
        self.logger.debug("Creating Channel: " + str(channel_index))
        channel = MCP3008Analog(mcp=self.mcp, channel_index=channel_index, hardware_serial_no=self.serial_no)
        self.channels.append(channel)
        return channel
