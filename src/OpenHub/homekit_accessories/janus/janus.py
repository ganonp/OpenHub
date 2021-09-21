import argparse
import asyncio
import logging
import random
import string
import time

import aiohttp

from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRecorder

pcs = set()


def transaction_id():
    return "".join(random.choice(string.ascii_letters) for x in range(12))


class JanusPlugin:
    def __init__(self, session, url):
        self._queue = asyncio.Queue()
        self._session = session
        self._url = url

    async def send(self, payload):
        message = {"janus": "message", "transaction": transaction_id(), "apisecret": "gardengnome"
                   }
        message.update(payload)
        async with self._session._http.post(self._url, json=message) as response:
            data = await response.json()
            assert data["janus"] == "ack"

        response = await self._queue.get()
        assert response["transaction"] == message["transaction"]
        return response


class JanusSession:
    def __init__(self, url):
        self._http = None
        self._poll_task = None
        self._plugins = {}
        self._root_url = url
        self._session_url = None

    async def attach(self, plugin_name: str) -> JanusPlugin:
        message = {
            "janus": "attach",
            "plugin": plugin_name,
            "transaction": transaction_id(),
            "apisecret": "gardengnome"
        }
        async with self._http.post(self._session_url, json=message) as response:
            data = await response.json()
            assert data["janus"] == "success"
            plugin_id = data["data"]["id"]
            plugin = JanusPlugin(self, self._session_url + "/" + str(plugin_id))
            self._plugins[plugin_id] = plugin
            return plugin

    async def create(self):
        self._http = aiohttp.ClientSession()
        message = {"janus": "create", "transaction": transaction_id(), "apisecret": "gardengnome"}
        async with self._http.post(self._root_url, json=message) as response:
            data = await response.json()
            assert data["janus"] == "success"
            session_id = data["data"]["id"]
            self._session_url = self._root_url + "/" + str(session_id)

        self._poll_task = asyncio.ensure_future(self._poll())

    async def destroy(self):
        if self._poll_task:
            self._poll_task.cancel()
            self._poll_task = None

        if self._session_url:
            message = {"janus": "destroy", "transaction": transaction_id(), "apisecret": "gardengnome"}
            async with self._http.post(self._session_url, json=message) as response:
                data = await response.json()
                assert data["janus"] == "success"
            self._session_url = None

        if self._http:
            await self._http.close()
            self._http = None

    async def _poll(self):
        while True:
            headers = {'Prefer': 'wait=30'}
            params = {"maxev": 1, 'apisecret': 'gardengnome'}
            async with self._http.get(self._session_url, headers=headers, params=params) as response:
                data = await response.json()
                if data["janus"] == "event":
                    plugin = self._plugins.get(data["sender"], None)
                    if plugin:
                        await plugin._queue.put(data)
                    else:
                        print(data)
            await asyncio.sleep(30)


recorder = MediaRecorder('/Users/ganonpierce/src/test/test0.mp4')


async def run(session):
    session = JanusSession("http://192.168.3.101:8088/janus")

    pc = RTCPeerConnection()

    await session.create()

    # join video room
    plugin = await session.attach("janus.plugin.streaming")
    response = await plugin.send(
        {
            "body": {"request": "watch",
                     "id": 1},
        }
    )
    print(response["plugindata"]["data"])
    # apply offer
    await pc.setRemoteDescription(
        RTCSessionDescription(
            sdp=response["jsep"]["sdp"], type=response["jsep"]["type"]
        )
    )

    # send answer
    await pc.setLocalDescription(await pc.createAnswer())

    print(str(pc.localDescription.sdp))
    response = await plugin.send(
        {
            "body": {"request": "start"},
            "jsep": {
                "sdp": pc.localDescription.sdp,
                "type": pc.localDescription.type
            },
        }
    )

    print(response)
    await recorder.start()


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Janus")
    # parser.add_argument("url", help="Janus root URL, e.g. http://localhost:8088/janus")
    # parser.add_argument(
    #     "--room",
    #     type=int,
    #     default=1234,
    #     help="The video room ID to join (default: 1234).",
    # ),
    # parser.add_argument("--play-from", help="Read the media from a file and sent it."),
    # parser.add_argument("--record-to", help="Write received media to a file."),
    # parser.add_argument("--verbose", "-v", action="count")
    # args = parser.parse_args()

    # if args.verbose:
    #     logging.basicConfig(level=logging.DEBUG)

    # create signaling and peer connection
    session = JanusSession("http://192.168.3.101:8088/janus")

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            run(session=session)
        )
    except KeyboardInterrupt:
        pass
    finally:

        if recorder is not None:
            loop.run_until_complete(recorder.stop())
        loop.run_until_complete(session.destroy())

        # close peer connections
        coros = [pc.close() for pc in pcs]
        loop.run_until_complete(asyncio.gather(*coros))

    while True:
        asyncio.sleep(1)

# DTLS HANDSHAKE DIFFERENT BETWEEN TWO PROBABLY ONLY HAPPENS WHEN YOU DO SOMETHING WITH THE TRACK (Or something that happens before you start using the track)