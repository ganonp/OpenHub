import asyncio
import glob
import os
from .hardware_interface import HardwareInterface
from .channels.mod_probe_temp import ModProbeTemp
import time
import logging

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

class ModProbe(HardwareInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, base_dir='/sys/bus/w1/devices/', device_file_name='/w1_slave', serial_no=None, channels=None,
                 *args, **kwargs):
        self.base_dir = base_dir
        self.device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = self.device_folder + device_file_name
        self.type = __name__
        super().__init__(serial_no, channels, *args, **kwargs)

    def create_channel(self):
        return {"mod": ModProbeTemp(self.device_file, self.serial_no)}

    async def read_temp_raw(self):
        while True:
            try:
                f = open(self.device_file, 'r')
                lines = f.readlines()
                f.close()
                return lines
            except IOError:
                self.logger.error("Unable to find modprobe device.")
                return -1
            except Exception as e:
                self.logger.error(str(e))
                await asyncio.sleep(1)

    async def read_temp_c(self):
        try:
            lines = await self.read_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                await asyncio.sleep(0.2)
                lines = await self.read_temp_raw()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos + 2:]
                return float(temp_string) / 1000.0
        except Exception as e:
            return float(-1)

    async def read_temp_f(self):
        temp_c = await self.read_temp_c()
        return temp_c * 9.0 / 5.0 + 32.0
