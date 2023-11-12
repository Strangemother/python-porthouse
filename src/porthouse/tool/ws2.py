import asyncio
from websockets import connect


url = 'ws://127.0.0.1:9004/1111'


async def hello(uri):
    websocket = await connect(uri)
    # async with connect(uri) as websocket:
    await websocket.send("Hello world!")
    await websocket.recv()
    await websocket.close()

asyncio.run(hello(url))
