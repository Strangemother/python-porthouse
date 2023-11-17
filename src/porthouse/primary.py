"""The "primary" is the access module to a running _router_.
This acts as the 'primary' receiver for an ingress, acting as the stepping-stone
into a router.

    run -> ingress -> primary -> router -> ...

Generally an ingress call upon `primary_ingress` to accept and loop listen to
websockets.

    import primary
    await primary.primary_ingress(websocket, token=token)

All arguments given through the `primary_ingress` head to the
`router.websocket_accept` method. If the websocket is accepted, it's handled until
disconnect.

All messages pipe to the router through the `handle_message` function:

    ok = await router.websocket_accept(websocket, **kw)
    data = await websocket.receive()
    ok = await handle_message(websocket, data)

"""
from contextlib import asynccontextmanager
import asyncio

from fastapi import WebSocket, FastAPI, Request

from loguru import logger
dlog = logger.debug

from .router import Router
from . import config as conf
from . import index_page
from . import adapters


router = Router()
adapter = adapters.get_adapter('starlette', router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    dlog('lifespan Startup')
    # await asyncio.sleep(3)
    # dlog('lifespan Startup - mount')
    await router.startup(app, adapter='starlette')
    yield
    dlog('lifespan shutdown')
    await router.shutdown(app)


async def primary_ingress(websocket, **kw):
    """The `primary_ingress` is the acceptor function for all incoming sockets.
    The router _accepts_ the socket then proceeds to wait for incoming mesages
    Upon a new message, call to the handle_message function
    """
    websocket._ok = await adapter.websocket_accept(websocket, **kw)
    # websocket._ok = await router.websocket_accept(websocket, **kw)

    while websocket._ok:
        # data = await router.receive()
        data = await adapter.wait_receive(websocket)
        ok = await adapter.handle_message(websocket, data)
        # ok = await handle_message(websocket, data)
    else:
        await adapter.wait_exit(websocket)
        # if websocket.client_state.value == 1:  # websocket.CONNECTED
        #     # await websocket.close()
        #     await adapter.close(websocket)
