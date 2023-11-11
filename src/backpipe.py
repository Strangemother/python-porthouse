import asyncio
from websockets import connect as w_connect

class BackPipe(object):

    def __init__(self, response_handler):
        self.queue = asyncio.Queue()
        self.socket = None
        self.response_handler = response_handler

    async def async_queue_put(self, data):
        return self.queue_put(data)

    def queue_put(self, data):
        self.queue.put_nowait(data)

    async def close(self):
        await self.socket.close()
        await asyncio.sleep(0)  # yield control to the event loop

    async def connect(self, uri):
        print('Connecting backpipe to', uri)
        self.socket = await w_connect(uri)
        # await handler(self.socket, self.consume, self.producer_handler)
        await self.send_wake()
        # self.queue_put('Hello.')
        await asyncio.sleep(0)  # yield control to the event loop
        # await self.producer_handler(self.socket)
        await self.consume(self.socket)

        return self.socket

    async def consume(self, websocket):
        async for message in websocket:
            # print('BackPipe message', message)
            await self.response_handler(message)
            # await websocket.send('Thank you.')

    async def producer_handler(self, websocket):
        while True:
            message = await self.queue.get()
            await websocket.send(message)
            self.queue.task_done()
        print('Joining queue')
        await self.queue.join()


    async def send_wake(self):
        message = 'Hello.'
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
