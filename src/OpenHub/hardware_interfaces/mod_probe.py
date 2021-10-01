import glob
import os
from .hardware_interface import HardwareInterface
from .channels.mod_probe_temp import ModProbeTemp
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

class ModProbe(HardwareInterface):

    def __init__(self, base_dir='/sys/bus/w1/devices/', device_file_name='/w1_slave', serial_no=None, channels=None,
                 *args, **kwargs):
        self.base_dir = base_dir
        self.device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = self.device_folder + device_file_name
        self.type = __name__
        super().__init__(serial_no, channels, *args, **kwargs)

    def create_channel(self):
        return {"mod": ModProbeTemp(self.device_file, self.serial_no)}

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp_c(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            return float(temp_string) / 1000.0

    def read_temp_f(self):
        temp_c = self.read_temp_c()
        return temp_c * 9.0 / 5.0 + 32.0
