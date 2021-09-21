import logging

from OpenHub import PiPicoGPI
import RPi.GPIO as GPIO


class PiGPI(PiPicoGPI):
    logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super(PiGPI, self).__init__(*args, **kwargs)
        GPIO.setup(self.pin, GPIO.IN)
