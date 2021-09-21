import logging

from OpenHub import PiPicoGPI


class PiPicoGPO(PiPicoGPI):
    logger = logging.getLogger(__name__)

    def __init__(self,default = 'off', *args, **kwargs):
        self.default = default
        super(PiPicoGPO, self).__init__(*args, **kwargs)
