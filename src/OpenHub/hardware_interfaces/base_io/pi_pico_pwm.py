import logging

from hardware_interfaces.base_io.base_io_interface import BaseIOInterface


class PiPicoPWM(BaseIOInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, pwm_pin=1, duty_min=0, duty_max=65025, freq=100, *args, **kwargs):
        self.pwm_pin = pwm_pin
        self.duty_min = duty_min
        self.duty_max = duty_max
        self.freq =freq
        super(PiPicoPWM, self).__init__(*args, **kwargs)
