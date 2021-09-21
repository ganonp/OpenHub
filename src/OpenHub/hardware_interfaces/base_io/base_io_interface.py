from abc import ABC, abstractmethod
import uuid
import logging


class BaseIOInterface(ABC):
    logger = logging.getLogger(__name__)

    def __init__(self, child_hardware_id=None, parent_hardware_id=None, *args, **kwargs):
        self.child_hardware_id = child_hardware_id
        self.parent_hardware_id = parent_hardware_id
