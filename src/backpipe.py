"""The BackPipe

A Backpipe is a Router's dedicated connect to another router. Other
routers may connect to this backpipe for ferrying messages between peers.

The router created a pipe when the server is connected. If the backpipe connect
connect, it assumes no back connection.
"""
import asyncio
from websockets import connect as w_connect
from websockets.exceptions import ConnectionClosedError

class BackPipe(object):

    def __init__(self, response_handler):
        self.queue = asyncio.Queue()
        self.socket = None
        self.response_handler = response_handler
        self.router_address = None

    async def async_queue_put(self, data):
        return self.queue_put(data)

    def queue_put(self, data):
        self.queue.put_nowait(data)

    async def close(self):
        if self.socket:
            await self.socket.close()
        await asyncio.sleep(0)  # yield control to the event loop

    def set_router_address(self, address:tuple):
        self.router_address = address

    async def connect(self, uri, raise_disconnect=False):
        print('Connecting backpipe to', uri)
        try:
            self.socket = await w_connect(uri)
        except ConnectionRefusedError:
            print('Cannot connect to backpipe - connection refused')
            return None

        await self.send_wake()

        await asyncio.sleep(0)  # yield control to the event loop
        # await self.producer_handler(self.socket)
        try:
            await self.consume(self.socket)
        except ConnectionClosedError as exc:
            print('Backpipe closed:', exc)
            if self.socket:
                await self.socket.close()
            if raise_disconnect:
                raise exc

        return self.socket

    async def consume(self, websocket):
        async for message in websocket:
            # print('BackPipe message', message)
            await self.response_handler(message)
            await asyncio.sleep(0)
            # await websocket.send('Thank you.')

    async def producer_handler(self, websocket):
        while True:
            message = await self.queue.get()
            await websocket.send(message)
            self.queue.task_done()
        print('Joining queue')
        await self.queue.join()


    async def send_wake(self):
        """Send the _wake word_ as a message to the peer.
        """
        message = 'Hello from {}'.format(self.router_address)
        print('Sending wake word.')
        await self.send(message)

    async def send(self, data):
        if self.socket:
            await self.socket.send(data)


# pipe = BackPipe()

# async def connect(uri):
#     await pipe.connect(uri)
#     return pipe

# async def close():
#     await pipe.close()
