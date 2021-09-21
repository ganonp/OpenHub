import logging
import signal
import resource
import asyncio

from pyhap.accessory_driver import AccessoryDriver
from pyhap.loader import Loader
from serial import Serial
from serial.tools import list_ports
from RPi import GPIO
import requests
import json

from OpenHub.globals import HAP_PYTHON_CHARACTERISTICS_FILE, HAP_PYTHON_SERVICES_FILE, HAP_PYTHON_ACCESSORIES_FILE
from hardware_interfaces.json import hardware_interface_decoder
from hardware_interfaces.channels.json.channel_decoder import ChannelDecoder
from OpenHub.globals import id_hardware_map, hardware_id_channels_map, id_channels_map, accessories, hub
import OpenHub.globals as glob

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

logging.basicConfig(level=logging.DEBUG, format="[%(module)s] %(message)s")


def get_pico_ports():
    pts = list(list_ports.comports())
    COMs = []
    for pt in pts:
        if 'ACM' in pt[0]:
            serial_port = Serial(pt.device, 9600, timeout=1)
            COMs.append(serial_port)
    return COMs


def setup_picos(COMS, hardwares, hardware_id_channels_map):

    print('FUCK')
    for ser in COMS:
        command = "init"
        ser.write(command.encode('utf-8'))
        pico_response = ser.readline()
        pico_serial = pico_response[:-2].decode('utf8').replace("'", '"')
        print(pico_serial)
        hardwares[pico_serial].set_serial_com(ser)

        channels_temp = []

        for channel in hardware_id_channels_map[pico_serial]:
            response = requests.get('http://192.168.3.132:8000/channels/' + str(channel.serial_no) + '/io')
            data = response.json()
            pico_config_element = {}
            pico_config_element['serial_no'] = channel.serial_no
            for datum in data:
                if 'label' in datum.keys() and datum['label'] is not None and 'pin' in datum.keys():
                    pico_config_element[datum['label']] = str(datum['pin'])
                pico_config_element = {**pico_config_element, **datum}
            from hardware_interfaces.channels.pi_pico_analog import PiPicoAnalog
            from hardware_interfaces.channels.pi_pico_pump import PiPicoPump
            if channel.__class__.__name__ == PiPicoAnalog.__name__:
                pico_config_element['type'] = 'sensor'
            elif channel.__class__.__name__ == PiPicoPump.__name__:
                pico_config_element['type'] = 'pump'
            else:
                pico_config_element['type'] = 'relay'
            pico_config_element['index'] = str(channel.channel_index)
            channels_temp.append(pico_config_element)

        pico_config = {'serial_no': pico_serial, 'no_channels': str(len(channels_temp)), 'channels': channels_temp}
        print((json.dumps(pico_config)))
        ser.write((json.dumps(pico_config) + '\n').encode())




def _gpio_setup(_cls, pin):
    if GPIO.mode() is None:
        GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)


def load_hub_config(hub):
    from homekit_accessories.json import homekit_decoder

    serial_no = 'efe3fcf0-6064-434f-9cf3-92098bba74ce'
    response = http.get('http://192.168.3.132:8000/hubs/' + serial_no)
    data = json.dumps(response.json())
    hub = json.loads(data, cls=homekit_decoder.HomekitDecoder)

    return hub


def load_hardware_config(hardware):
    response = http.get('http://192.168.3.132:8000/hardwares')
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
    from homekit_accessories.json import homekit_decoder

    response = requests.get('http://192.168.3.132:8000/accessories')
    data = json.dumps(response.json())
    accessories_temp = json.loads(data, cls=homekit_decoder.HomekitDecoder)
    for accessory in accessories_temp:
        accessories[accessory.serial_no] = accessory
    return accessories


def setup_accessories(hub, accessories):
    for accessory in accessories.values():
        hub.add_accessory(accessory)
    glob.driver.add_accessory(accessory=hub)

    # driver.add_accessory(accessory)


#
# def load_calibration_config(data):
#     global calibration
#     calibration = json.loads(str(data), cls=raw_value_decoder.RawValueDecoder)

id_hardware_map = load_hardware_config(id_hardware_map)

hardware_id_channels_map, id_channels_map = load_channels(hardware_id_channels_map, id_channels_map)

COMS = get_pico_ports()
setup_picos(COMS, id_hardware_map, hardware_id_channels_map)



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
glob.loader = Loader(path_char=HAP_PYTHON_CHARACTERISTICS_FILE,
                path_service=HAP_PYTHON_SERVICES_FILE)

glob.driver = AccessoryDriver(port=51826, persist_file=HAP_PYTHON_ACCESSORIES_FILE,
                         loader=glob.loader)

hub = load_hub_config(hub)

accessories = load_homekit_accessory_config(accessories)
setup_accessories(hub, accessories)

resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

signal.signal(signal.SIGTERM, glob.driver.signal_handler)

glob.driver.start()
