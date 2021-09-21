import logging

from OpenHub import PiPicoGPO
import RPi.GPIO as GPIO


class PiGPO(PiPicoGPO):
    logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super(PiGPO, self).__init__(*args, **kwargs)
        GPIO.setup(self.pin, GPIO.OUT)
        if self.default == 'on':
            GPIO.output(self.pin, GPIO.HIGH)
        elif self.default == 'off':
            GPIO.output(self.pin, GPIO.LOW)
