import asyncio

from OpenHub.homekit_accessories.homkit_sensor_interface import HomeKitSensorInterface
import logging
from OpenHub.globals import driver
from pyhap.const import CATEGORY_CAMERA
from pyhap.camera import Camera as PyHapCamera, STREAMING_STATUS, SELECTED_STREAM_CONFIGURATION_TYPES, RTP_PARAM_TYPES, \
    AUDIO_CODEC_PARAM_TYPES, AUDIO_TYPES, VIDEO_TYPES, VIDEO_CODEC_PARAM_TYPES, VIDEO_ATTRIBUTES_TYPES
from pyhap import tlv, util
from pyhap.camera import SETUP_TYPES, SETUP_ADDR_INFO, SETUP_SRTP_PARAM, SETUP_STATUS, NO_SRTP, SRTP_CRYPTO_SUITES
from pyhap.camera import VIDEO_CODEC_PARAM_PROFILE_ID_TYPES, VIDEO_CODEC_PARAM_LEVEL_TYPES
from uuid import UUID
import struct
import os
import time
import base64

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
            "srtp": True,

            # hard code the address if auto-detection does not work as desired: e.g. "192.168.1.226"
            "address": util.get_local_address(),
            'start_stream_cmd': (
                "gst-launch-1.0 v4l2src ! "
                "video/x-h264, width={width},height={height},framerate={fps}/1 ! "
                "h264parse ! rtph264pay pt=99 ssrc={v_ssrc} ! "
                "srtpenc key={v_srtp_key} rtp-cipher=\"aes-128-icm\" rtp-auth=\"hmac-sha1-80\" ! "
                "udpsink sync=false host={address} port={v_port}")
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



    async def start_stream(self, session_info, stream_config):
        """Start a new stream with the given configuration.

        This method can be implemented to start a new stream. Any specific information
        about the started stream can be persisted in the ``session_info`` argument.
        The same will be passed to ``stop_stream`` when the stream for this session
        needs to be stopped.

        The default implementation starts a new process with the command in
        ``self.start_stream_cmd``, formatted with the ``stream_config``.

        :param session_info: Contains information about the current session. Can be used
            for session storage. Available keys:
            - id - The session ID.
        :type session_info: ``dict``
        :param stream_config: Stream configuration, as negotiated with the HAP client.
            Implementations can only use part of these. Available keys:
            General configuration:
                - address - The IP address from which the camera will stream
                - v_port - Remote port to which to stream video
                - v_srtp_key - Base64-encoded key and salt value for the
                    AES_CM_128_HMAC_SHA1_80 cipher to use when streaming video.
                    The key and the salt are concatenated before encoding
                - a_port - Remote audio port to which to stream audio
                - a_srtp_key - As v_srtp_params, but for the audio stream.
            Video configuration:
                - v_profile_id - The profile ID for the H.264 codec, e.g. baseline.
                    Refer to ``VIDEO_CODEC_PARAM_PROFILE_ID_TYPES``.
                - v_level - The level in the profile ID, e.g. 3:1.
                    Refer to ``VIDEO_CODEC_PARAM_LEVEL_TYPES``.
                - width - Video width
                - height - Video height
                - fps - Video frame rate
                - v_ssrc - Video synchronisation source
                - v_payload_type - Type of the video codec
                - v_max_bitrate - Maximum bit rate generated by the codec in kbps
                    and averaged over 1 second
                - v_rtcp_interval - Minimum RTCP interval in seconds
                - v_max_mtu - MTU that the IP camera must use to transmit
                    Video RTP packets.
            Audio configuration:
                - a_bitrate - Whether the bitrate is variable or constant
                - a_codec - Audio codec
                - a_comfort_noise - Wheter to use a comfort noise codec
                - a_channel - Number of audio channels
                - a_sample_rate - Audio sample rate in KHz
                - a_packet_time - Length of time represented by the media in a packet
                - a_ssrc - Audio synchronisation source
                - a_payload_type - Type of the audio codec
                - a_max_bitrate - Maximum bit rate generated by the codec in kbps
                    and averaged over 1 second
                - a_rtcp_interval - Minimum RTCP interval in seconds
                - a_comfort_payload_type - The type of codec for comfort noise

        :return: True if and only if starting the stream command was successful.
        :rtype: ``bool``
        """
        logger.debug(
            '[%s] Starting stream with the following parameters: %s',
            session_info['id'],
            stream_config
        )
        stream_config_temp = stream_config.copy()
        stream_config_temp['v_srtp_key'] = base64.b64decode(stream_config_temp['v_srtp_key']).hex()

        cmd = self.start_stream_cmd.format(**stream_config_temp).split()
        logger.debug('Executing start stream command: "%s"', ' '.join(cmd))

        if self._streaming_status[stream_config_temp['stream_idx']] == STREAMING_STATUS['STREAMING']:
            await self.stop_stream(session_info)

        try:
            process = await asyncio.create_subprocess_exec(*cmd,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.PIPE,
                    limit=1024)
        except Exception as e:  # pylint: disable=broad-except
            logger.error('Failed to start streaming process because of error: %s', e)
            return False

        session_info['process'] = process

        logger.info(
            '[%s] Started stream process - PID %d',
            session_info['id'],
            process.pid
        )
        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=2.0)
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')
            return False
        return True

    async def stop_stream(self, session_info):  # pylint: disable=no-self-use
        """Stop the stream for the given ``session_id``.

        This method can be implemented if custom stop stream commands are needed. The
        default implementation gets the ``process`` value from the ``session_info``
        object and terminates it (assumes it is a ``subprocess.Popen`` object).

        :param session_info: The session info object. Available keys:
            - id - The session ID.
        :type session_info: ``dict``
        """
        session_id = session_info['id']
        ffmpeg_process = session_info.get('process')
        if ffmpeg_process:
            logger.info('[%s] Stopping stream.', session_id)
            try:
                ffmpeg_process.terminate()
                _, stderr = await asyncio.wait_for(
                    ffmpeg_process.communicate(), timeout=2.0)
                logger.debug('Stream command stderr: %s', stderr)
            except asyncio.TimeoutError:
                logger.error(
                    'Timeout while waiting for the stream process '
                    'to terminate. Trying with kill.'
                )
                ffmpeg_process.kill()
                await ffmpeg_process.wait()
            except Exception as e:
                logger.error(
                    str(e)
                )
                ffmpeg_process.kill()
                await ffmpeg_process.wait()
            logger.debug('Stream process stopped.')
        else:
            logger.warning('No process for session ID %s', session_id)


    async def _start_stream(self, objs, reconfigure):  # pylint: disable=unused-argument
        """Start or reconfigure video streaming for the given session.

        Schedules ``self.start_stream`` or ``self.reconfigure``.

        No support for reconfigure currently.

        :param objs: TLV-decoded SelectedRTPStreamConfiguration
        :type objs: ``dict``

        :param reconfigure: Whether the stream should be reconfigured instead of
            started.
        :type reconfigure: bool
        """
        video_tlv = objs.get(SELECTED_STREAM_CONFIGURATION_TYPES['VIDEO'])
        audio_tlv = objs.get(SELECTED_STREAM_CONFIGURATION_TYPES['AUDIO'])

        opts = {}

        if video_tlv:
            video_objs = tlv.decode(video_tlv)

            video_codec_params = video_objs.get(VIDEO_TYPES['CODEC_PARAM'])
            if video_codec_params:
                video_codec_param_objs = tlv.decode(video_codec_params)
                opts['v_profile_id'] = \
                    video_codec_param_objs[VIDEO_CODEC_PARAM_TYPES['PROFILE_ID']]
                opts['v_level'] = \
                    video_codec_param_objs[VIDEO_CODEC_PARAM_TYPES['LEVEL']]

            video_attrs = video_objs.get(VIDEO_TYPES['ATTRIBUTES'])
            if video_attrs:
                video_attr_objs = tlv.decode(video_attrs)
                opts['width'] = struct.unpack('<H',
                            video_attr_objs[VIDEO_ATTRIBUTES_TYPES['IMAGE_WIDTH']])[0]
                opts['height'] = struct.unpack('<H',
                            video_attr_objs[VIDEO_ATTRIBUTES_TYPES['IMAGE_HEIGHT']])[0]
                opts['fps'] = struct.unpack('<B',
                                video_attr_objs[VIDEO_ATTRIBUTES_TYPES['FRAME_RATE']])[0]

            video_rtp_param = video_objs.get(VIDEO_TYPES['RTP_PARAM'])
            if video_rtp_param:
                video_rtp_param_objs = tlv.decode(video_rtp_param)
                if RTP_PARAM_TYPES['SYNCHRONIZATION_SOURCE'] in video_rtp_param_objs:
                    opts['v_ssrc'] = struct.unpack('<I',
                        video_rtp_param_objs.get(
                            RTP_PARAM_TYPES['SYNCHRONIZATION_SOURCE']))[0]
                if RTP_PARAM_TYPES['PAYLOAD_TYPE'] in video_rtp_param_objs:
                    opts['v_payload_type'] = \
                        video_rtp_param_objs.get(RTP_PARAM_TYPES['PAYLOAD_TYPE'])
                if RTP_PARAM_TYPES['MAX_BIT_RATE'] in video_rtp_param_objs:
                    opts['v_max_bitrate'] = struct.unpack('<H',
                        video_rtp_param_objs.get(RTP_PARAM_TYPES['MAX_BIT_RATE']))[0]
                if RTP_PARAM_TYPES['RTCP_SEND_INTERVAL'] in video_rtp_param_objs:
                    opts['v_rtcp_interval'] = struct.unpack('<f',
                        video_rtp_param_objs.get(RTP_PARAM_TYPES['RTCP_SEND_INTERVAL']))[0]
                if RTP_PARAM_TYPES['MAX_MTU'] in video_rtp_param_objs:
                    opts['v_max_mtu'] = video_rtp_param_objs.get(RTP_PARAM_TYPES['MAX_MTU'])

        if audio_tlv:
            audio_objs = tlv.decode(audio_tlv)

            opts['a_codec'] = audio_objs[AUDIO_TYPES['CODEC']]
            audio_codec_param_objs = tlv.decode(
                                        audio_objs[AUDIO_TYPES['CODEC_PARAM']])
            audio_rtp_param_objs = tlv.decode(
                                        audio_objs[AUDIO_TYPES['RTP_PARAM']])
            opts['a_comfort_noise'] = audio_objs[AUDIO_TYPES['COMFORT_NOISE']]

            opts['a_channel'] = \
                audio_codec_param_objs[AUDIO_CODEC_PARAM_TYPES['CHANNEL']][0]
            opts['a_bitrate'] = struct.unpack('?',
                audio_codec_param_objs[AUDIO_CODEC_PARAM_TYPES['BIT_RATE']])[0]
            opts['a_sample_rate'] = 8 * (
                1 + audio_codec_param_objs[AUDIO_CODEC_PARAM_TYPES['SAMPLE_RATE']][0])
            opts['a_packet_time'] = struct.unpack('<B',
                audio_codec_param_objs[AUDIO_CODEC_PARAM_TYPES['PACKET_TIME']])[0]

            opts['a_ssrc'] = struct.unpack('<I',
                audio_rtp_param_objs[RTP_PARAM_TYPES['SYNCHRONIZATION_SOURCE']])[0]
            opts['a_payload_type'] = audio_rtp_param_objs[RTP_PARAM_TYPES['PAYLOAD_TYPE']]
            opts['a_max_bitrate'] = struct.unpack('<H',
                audio_rtp_param_objs[RTP_PARAM_TYPES['MAX_BIT_RATE']])[0]
            opts['a_rtcp_interval'] = struct.unpack('<f',
                audio_rtp_param_objs[RTP_PARAM_TYPES['RTCP_SEND_INTERVAL']])[0]
            opts['a_comfort_payload_type'] = \
                audio_rtp_param_objs[RTP_PARAM_TYPES['COMFORT_NOISE_PAYLOAD_TYPE']]

        session_objs = tlv.decode(objs[SELECTED_STREAM_CONFIGURATION_TYPES['SESSION']])
        session_id = UUID(bytes=session_objs[SETUP_TYPES['SESSION_ID']])
        session_info = self.sessions[session_id]
        stream_idx = session_info['stream_idx']

        opts.update(session_info)
        success = await self.reconfigure_stream(session_info, opts) if reconfigure \
            else await self.start_stream(session_info, opts)

        if success:
            self._streaming_status[stream_idx] = STREAMING_STATUS['STREAMING']
        else:
            logger.error(
                '[%s] Failed to start/reconfigure stream, deleting session.',
                session_id
            )
            self._streaming_status[stream_idx] = STREAMING_STATUS['AVAILABLE']
            del self.sessions[session_id]
