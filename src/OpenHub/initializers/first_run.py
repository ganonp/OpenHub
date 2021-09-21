from .hardware import first_time_setup
from .homekit_interfaces import first_time_kit_setup
from OpenHub.globals import id_hardware_map


def first_run():
    first_time_kit_setup.first_run()
    first_time_setup.first_run()
    for component in id_hardware_map:
        interface_channel_with_homekit_accessory(component)