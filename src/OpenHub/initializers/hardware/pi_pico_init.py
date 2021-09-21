import json

import serial

from hardware_interfaces.pi_pico import PiPico
from Adafruit_GPIO import GPIO
from homekit_accessories.liquid_level_sensor import LiquidLevelSensor
from homekit_accessories.etape import ETapeSensor
from homekit_accessories.pressure_sensor import PressureSensor
from homekit_accessories import Pump


class PiPicoInit():
    interrupts = [2, 3, 17]
    pico_configs = []
    COMs = []
    picos = []
    pico_sensor_serial_no_to_serial_com = {}

    def init_picos(self):
        self.get_pico_ports()
        self.setup_interrupt_to_acm_mapping()


    def get_pico_ports(self):
        pts = list(serial.tools.list_ports.comports())

        for pt in pts:
            if 'ACM' in pt[0]:
                self.COMs.append(pt[0])

    def setup_interrupt_to_acm_mapping(self):

        for interrupt in self.interrupts:
            GPIO.setup(interrupt, GPIO.OUT)
            GPIO.output(interrupt, GPIO.HIGH)

        for ser in self.COMs:
            command = "init" + "\n"
            ser.write(command.encode('utf-8'))
            pico_data = ser.readline()
            sensor_response = pico_data[:-2]
            print(sensor_response)
            pico_config = json.loads(sensor_response)
            pico_config['serial_com'] = ser
            self.pico_configs.append(pico_config)

        for interrupt in self.interrupts:
            GPIO.output(interrupt, GPIO.LOW)

    def initialize_picos(self, sensor_hub):
        for pico_config in self.pico_configs:
            pico = PiPico(pico_config)
            self.picos.append(pico)

    def setup_pico_sensors(self, sensor_hub):
        for pico in self.picos:
            for channel in pico.hardware_id_channels_map:
                type = channel['type']
                sensor = None
                if type == 'optical':
                    sensor = LiquidLevelSensor(pico)
                elif type == 'etape':
                    sensor = ETapeSensor(pico)
                elif type == 'pressure':
                    sensor = PressureSensor(pico)
                elif type == 'pump':
                    sensor = Pump(pico)
                if sensor is not None:
                    sensor_hub.add_accessory(sensor)
