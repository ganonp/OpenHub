from hardware_interfaces import mod_probe, dht22, mcp3008, veml_7700
from initializers.homekit_interfaces.first_time_kit_setup import interface_channel_with_homekit_accessory
import board


def configure_dht22(sensor_hub):
    num_dht22s = int(input("How many DHT22s (humidity/temperature) are connected? ")) or 0
    for i in range(num_dht22s):
        gpio_pin = int(input("Which gpio pin is this connected to? ")) or board.D17
        dht22_interface = dht22.DHT22(gpio_pin)
        sensor_hub.id_hardware_map.append(dht22_interface)


def configure_mcp3008(sensor_hub):
    num_mcp3008s = int(input("How many MCP3008s (analog to digital converter) are connected? "))
    if num_mcp3008s > 0:
        for i in range(num_mcp3008s):
            # sck = board.SCK, miso = board.MISO, mosi = board.MOSI, cs_pin = board.D5
            sck = int(input("Which pin is sck? ")) or board.SCK
            miso = int(input("Which pin is miso? ")) or board.MISO
            mosi = int(input("Which pin is mosi? ")) or board.MOSI
            cs_pin = int(input("Which pin is cs_pin? ")) or board.D5
            mcp3008_interface = mcp3008.MCP3008(sck=sck, miso=miso, mosi=mosi, cs_pin=cs_pin)
            sensor_hub.id_hardware_map.append(mcp3008_interface)

            num_channels = int(input("How many channels of the MCP3008 are you using?"))
            for j in range(num_channels):
                channel = mcp3008_interface.create_analog_channel()
                interface_channel_with_homekit_accessory(channel)


def configure_mod_probe(sensor_hub):
    num_mod_probe = int(input("How many modprobes (soil temp) are connected? ")) or 0
    for i in range(num_mod_probe):
        mod_probe_interface = mod_probe.ModProbe()
        channel = mod_probe_interface.create_channel()
        interface_channel_with_homekit_accessory(channel)
        sensor_hub.id_hardware_map.append(mod_probe_interface)


def configure_pi_picos(sensor_hub):
    global interrupts
    num_pi_picos = int(input("How many pi picos are connected? "))
    for i in range(num_pi_picos):
        interrupt = int(input("Enter one interrupt pin: "))
        interrupts.append(interrupt)


def configure_veml(sensor_hub):
    num_veml = int(input("How many veml (light sensor) are connected? "))
    for i in range(num_veml):
        scl = int(input("Which pin is scl? ")) or board.SCL
        sda = int(input("Which pin is sda? ")) or board.SDA
        veml7700_interface = veml_7700.VEML7700(scl, sda)
        sensor_hub.id_hardware_map.append(veml7700_interface)


def first_run(sensor_hub):
    configure_dht22(sensor_hub)
    configure_veml(sensor_hub)
    configure_pi_picos(sensor_hub)
    configure_mod_probe(sensor_hub)
    configure_mcp3008()