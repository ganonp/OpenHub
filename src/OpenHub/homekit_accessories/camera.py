import asyncio

from OpenHub.homekit_accessories.homkit_sensor_interface import HomeKitSensorInterface
import logging
from OpenHub.globals import driver
from pyhap.const import CATEGORY_CAMERA
from pyhap.camera import Camera as PyHapCamera
from pyhap import tlv
from pyhap.camera import SETUP_TYPES,SETUP_ADDR_INFO,SETUP_SRTP_PARAM,SETUP_STATUS,NO_SRTP,SRTP_CRYPTO_SUITES
from pyhap.camera import VIDEO_CODEC_PARAM_PROFILE_ID_TYPES, VIDEO_CODEC_PARAM_LEVEL_TYPES
from uuid import UUID
import struct
import os
import time

from pyhap.util import to_base64_str

logger = logging.getLogger(__name__)


class Camera(PyHapCamera):
    run_debug_message = "Camera State: "

    category = CATEGORY_CAMERA

    def __init__(self, serial_no=None, display_name=None, *args, **kwargs):
        self.category = CATEGORY_CAMERA

        options = {
            "video": {
                "codec": {
                    "profiles": [
                        VIDEO_CODEC_PARAM_PROFILE_ID_TYPES["BASELINE"],
                        VIDEO_CODEC_PARAM_PROFILE_ID_TYPES["MAIN"],
                        VIDEO_CODEC_PARAM_PROFILE_ID_TYPES["HIGH"]
                    ],
                    "levels": [
                        VIDEO_CODEC_PARAM_LEVEL_TYPES['TYPE3_1'],
                        VIDEO_CODEC_PARAM_LEVEL_TYPES['TYPE3_2'],
                        VIDEO_CODEC_PARAM_LEVEL_TYPES['TYPE4_0'],
                    ],
                },
                "resolutions": [
                    # Width, Height, framerate
                    [320, 240, 15],  # Required for Apple Watch
                    [1024, 768, 30],
                    [640, 480, 30],
                    [640, 360, 30],
                    [480, 360, 30],
                    [480, 270, 30],
                    [320, 240, 30],
                    [320, 180, 30],
                ],
            },
            "audio": {
                "codecs": [
                    {
                        'type': 'OPUS',
                        'samplerate': 24,
                    },
                    {
                        'type': 'AAC-eld',
                        'samplerate': 16
                    }
                ],
            },
            "srtp": False,

            # hard code the address if auto-detection does not work as desired: e.g. "192.168.1.226"
            "address": "http://192.168.3.101:8088/janus",
            'start_stream_cmd': ('gst-launch-1.0 v4l2src ! video/x-h264, '
                                 'width=640, '
                                 'height=480, '
                                 'framerate=30/1 '
                                 '! h264parse ! '
                                 'rtph264pay config-interval=1 pt=96 ! '
                                 'udpsink sync=false host=192.168.3.101 port=8004')
        }


        self.display_name = self.set_display_name(display_name)
        self.serial_no = serial_no

        super().__init__(options=options, driver=driver, display_name=self.display_name, *args, **kwargs)
        # super(HomeKitSensorInterface, self).__init__(serial_no=serial_no, display_name=display_name, *args,
        #                                              **kwargs)

    def set_display_name(self, display_name):
        if display_name is None:
            return "Camera"
        else:
            return display_name

    # def add_functional_service(self):
    #     return self.add_preload_service('C')
    #
    # def add_functional_service_characteristic(self):
    #     # return self.service.configure_char(
    #     #     'On', setter_callback=self.set_relay)
    #     pass
    #     # ### For client extensions ###

    async def async_get_snapshot(self, image_size):  # pylint: disable=unused-argument, no-self-use
        """Return a jpeg of a snapshot from the camera.
        Overwrite to implement getting snapshots from your camera.
        :param image_size: ``dict`` describing the requested image size. Contains the
            keys "image-width" and "image-height"
        """
        width = str(image_size["image-width"])
        height = str(image_size["image-height"])
        command = 'raspistill -w ' + width + ' -h ' +height + ' -e jpg -o /home/openhubdaemon/snapshot.jpg'
        logger.info('Executing get snapshotd: "%s"', ' '.join(command))
        try:
            f = os.stat('/home/openhubdaemon/snapshot.jpg')
            time_since_update = int(time.time()) - f.st_mtime
            if time_since_update > 1000:
                await asyncio.create_subprocess_shell(command,
                                                               stdout=asyncio.subprocess.DEVNULL,
                                                               stderr=asyncio.subprocess.DEVNULL,
                                                               limit=1024)
            with open("""/home/openhubdaemon/snapshot.jpg""", 'rb') as fp:
                return fp.read()
        except Exception as e:  # pylint: disable=broad-except
            logger.info('Failed to get snapshot: %s', e)
            with open("""/home/openhubdaemon/fallback.jpg""", 'rb') as fp:
                return fp.read()

