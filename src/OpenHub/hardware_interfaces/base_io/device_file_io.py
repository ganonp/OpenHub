import logging
import glob
from hardware_interfaces.base_io.base_io_interface import BaseIOInterface


class DeviceFileIO(BaseIOInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, base_dir='/sys/bus/w1/devices/', device_file_name='/w1_slave', *args, **kwargs):
        self.base_dir = base_dir
        self.device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = self.device_folder + device_file_name

        super(DeviceFileIO, self).__init__(*args, **kwargs)







