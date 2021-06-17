import logging
import signal
import resource
import asyncio, socket

from requests.packages.urllib3.util.retry import Retry
from serial import Serial
from serial.tools import list_ports
from RPi import GPIO
from websockets import connect
import requests
import json

from OpenHub.calibrators.json import raw_value_decoder
from OpenHub.hardware_interfaces.json import hardware_interface_decoder
from OpenHub.hardware_interfaces.channels.json.channel_decoder import ChannelDecoder
from OpenHub.homekit_accessories.json import homekit_decoder
from OpenHub.globals import id_hardware_map, hardware_id_channels_map, id_channels_map, accessories, driver, \
    hub

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=10,
    backoff_factor=10,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")


def get_pico_ports():
    pts = list(list_ports.comports())
    COMs = []
    for pt in pts:
        if 'ACM' in pt[0]:
            serial_port = Serial(pt.device, 9600, timeout=1)
            COMs.append(serial_port)
    return COMs


def setup_interrupt_to_acm_mapping(COMS, hardwares):
    for hardware in hardwares.values():
        if type(hardware).__name__ == 'PiPico':
            GPIO.setup(hardware.interrupt, GPIO.OUT)
            GPIO.output(hardware.interrupt, GPIO.LOW)

    for hardware in hardwares.values():
        if type(hardware).__name__ == 'PiPico':
            GPIO.output(hardware.interrupt, GPIO.HIGH)

    for ser in COMS:
        command = "init"
        ser.write(command.encode('utf-8'))
        pico_data = ser.readline()
        sensor_response = pico_data[:-2]
        print(sensor_response)
        pico_config = json.loads(sensor_response.decode('utf8').replace("'", '"'))
        hardwares[pico_config['serial_no']].set_serial_com(ser)

    for hardware in hardwares.values():
        if type(hardware).__name__ == 'PiPico':
            GPIO.output(hardware.interrupt, GPIO.LOW)


def _gpio_setup(_cls, pin):
    if GPIO.mode() is None:
        GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)


def load_hub_config(hub):
    serial_no = 'efe3fcf0-6064-434f-9cf3-92098bba74ce'
    response = http.get('http://192.168.3.132:8000/hubs/' + serial_no)
    data = json.dumps(response.json())
    hub = json.loads(data, cls=homekit_decoder.HomekitDecoder)

    return hub


def load_hardware_config(hardware):
    response = requests.get('http://192.168.3.132:8000/hardwares')
    data = json.dumps(response.json())
    hardware_temp = json.loads(data, cls=hardware_interface_decoder.HardwareDecoder)
    for hard_t in hardware_temp:
        hardware['id'] = hard_t
    return hardware


def load_channels(channels, id_channels_map):
    for hard in id_hardware_map.values():
        response = requests.get('http://192.168.3.132:8000/hardwares/' + str(hard.serial_no) + '/channels')
        data = json.dumps(response.json())
        t = []
        for channel in response.json():
            t.append(json.loads(json.dumps(channel), cls=ChannelDecoder))
        channels[str(hard.serial_no)] = t
    for hard in id_hardware_map.values():
        for channel in channels[str(hard.serial_no)]:
            id_channels_map[channel.serial_no] = channel

    return channels, id_channels_map


def load_homekit_accessory_config(accessories):
    response = requests.get('http://192.168.3.132:8000/accessories')
    data = json.dumps(response.json())
    accessories_temp = json.loads(data, cls=homekit_decoder.HomekitDecoder)
    for accessory in accessories_temp:
        accessories[accessory.serial_no] = accessory
    return accessories


def setup_accessories(hub, accessories):
    for accessory in accessories.values():
        hub.add_accessory(accessory)
    driver.add_accessory(accessory=hub)

    # driver.add_accessory(accessory)


#
# def load_calibration_config(data):
#     global calibration
#     calibration = json.loads(str(data), cls=raw_value_decoder.RawValueDecoder)

hub = load_hub_config(hub)
id_hardware_map = load_hardware_config(id_hardware_map)

COMS = get_pico_ports()
setup_interrupt_to_acm_mapping(COMS, id_hardware_map)

hardware_id_channels_map, id_channels_map = load_channels(hardware_id_channels_map, id_channels_map)
accessories = load_homekit_accessory_config(accessories)
setup_accessories(hub, accessories)

resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))


async def handle_client(reader, writer):
    request = None
    while request != 'quit':
        request = (await reader.readline())
        print(str(request))
        response = str(eval(request)) + '\n'
        print(str(response))
        writer.write(response.encode('utf8'))
        await writer.drain()
    writer.close()


async def run_server():
    server = await asyncio.start_server(handle_client, 'localhost', 8888)
    async with server:
        await server.serve_forever()


# asyncio.run(run_server())

#
# def get_bridge(driver):
#     bridge = GardenBridge.GardenBridge(driver)
#
#     return bridge
#
#
signal.signal(signal.SIGTERM, driver.signal_handler)

driver.start()
