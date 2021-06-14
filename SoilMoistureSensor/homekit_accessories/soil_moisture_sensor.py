import logging
from SoilMoistureSensor.homekit_accessories.homkit_sensor_interface import HomeKitSensorInterface
from SoilMoistureSensor.calibrators.soil_moisture_voltage_converter import SoilMoistureVoltageConverter


class SoilMoistureSensor(HomeKitSensorInterface):
    logger = logging.getLogger(__name__)
    run_debug_message = "Current Soil Moisture: "

    def __init__(self, calibrator=SoilMoistureVoltageConverter(), serial_no=None, display_name=None,
                 channel_interface_serial_no=None, *args, **kwargs):
        self.add_name()
        super().__init__(raw_value_converter=calibrator, serial_no=serial_no, display_name=display_name,
                         channel_interface_serial_no=channel_interface_serial_no, *args, **kwargs)


    def set_display_name(self, display_name):
        if self.display_name is None:
            return display_name + "SoilMoisture"

    def add_name(self):
        if self.display_name is None:
            self.display_name = input(
                "Please Add Display Name for Sensor on Channel: " + str(self.index)) or "SoilMoistureDisplayName" + str(
                self.index)

    def add_functional_service(self):
        return self.add_preload_service("SoilMoistureSensor")

    def add_functional_service_characteristic(self):
        return self.service.get_characteristic('SoilMoisture')
    #
    # async def run(self):
    #     voltage = mcpi.get_voltage_for_channel(int(self.index))
    #     self.logger.debug("Voltage: " + str(voltage))
    #     self.set_min_max_voltage(voltage)
    #     output = self.convert_voltage_to_output()
    #     self.logger.debug("Output / Moisture Level: " + str(output))
    #     self.soil_moisture.set_value(output)
    #     # await asyncio.sleep(1)
