from .channel_interface import ChannelInterface
import logging
import asyncio
from OpenHub.globals import id_hardware_map
from adafruit_motor import stepper


class AdafruitStepperMotor(ChannelInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, config, hardware_serial_no=None, serial_no=None,channel_stats=None, *args, **kwargs):
        self.adafruit_stepper_motor_hat = id_hardware_map[config['hardware']]
        self.serial_no = config['id']
        self.type = config['type']
        self.motor_index = config['channel_index']
        self.stepper_motor = None
        if self.motor_index == 1:
            self.stepper_motor = self.adafruit_stepper_motor_hat.kit.stepper1
        elif self.motor_index == 2:
            self.stepper_motor = self.adafruit_stepper_motor_hat.kit.stepper2

        super().__init__(config=config,hardware_serial_no=self.adafruit_stepper_motor_hat.serial_no, serial_no=self.serial_no, *args, **kwargs)

    def setup(self,config):
        self.full_rotation_steps = config['full_rotation_steps']
        self.number_of_rotations = config['number_of_rotations']
        self.steps = int(self.full_rotation_steps * self.number_of_rotations)
        self.step_pause_time = config['step_pause_time']



    async def turn_on(self):
        for i in range(self.steps):
            self.stepper_motor.onestep()
            await asyncio.sleep(self.step_pause_time)

    async def turn_off(self):
        for i in range(self.steps):
            self.stepper_motor.onestep(direction=stepper.BACKWARD)
            await asyncio.sleep(self.step_pause_time)

    async def get_raw_data(self):
        pass
