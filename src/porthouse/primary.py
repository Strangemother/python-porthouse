"""The "primary" is the access module to a running _router_.
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


router = Router()


def generate_typemap():
    """Return a dict to map actions to methods. The key should be data['type']
    If the data[type] is not mapped within this dict
    """
    return {
        'websocket.disconnect': websocket_disconnect,
        'default': default_action,
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    dlog('lifespan Startup')
    # await asyncio.sleep(3)
    # dlog('lifespan Startup - mount')
    await router.startup(app)
    yield
    dlog('lifespan shutdown')
    await router.shutdown(app)


async def primary_ingress(websocket, **kw):
    """The `primary_ingress` is the acceptor function for all incoming sockets.
    The router _accepts_ the socket then proceeds to wait for incoming mesages
    Upon a new message, call to the handle_message function
    """
    websocket._ok = await router.websocket_accept(websocket, **kw)

    while websocket._ok:
        data = await websocket.receive()
        ok = await handle_message(websocket, data)
    else:
        if websocket.client_state.value == 1:  # websocket.CONNECTED
            await websocket.close()


async def handle_message(websocket, data):
    """Given a socket and the new message, read the `type` of message
    and call the `typemap` handler function. If no function is found use
    the `default_action` function.
    If the result from the action method is not a truthy, the socket will
    disconnect.

    Return an `ok` truthy. `0` for _not ok_, `1` for okay.
    """
    action_func = typemap.get(data['type'], None) or typemap['default']
    ok = await action_func(websocket, data)
    return ok


async def default_action(websocket, data):
    """The default function for an incoming message from a websocket.
    Call to the router recv_socket_event and return a _receipt_ back to the
    client (if given).

    Return `1` or any truthy as an "ok" to _continue listening_.
    """
    receipt = await router.recv_socket_event(websocket, data)
    # 'send', 'send_bytes', 'send_json', 'send_text',
    if receipt is not None:
        await websocket.send_text(receipt)
    return 1


async def websocket_disconnect(websocket, data):
    """Handle the "websocket.disconnect" event from the primary ingress.
    Call upon the router websocket_disconnect method and flag the websocket as
    not _ok_.
    """
    websocket._ok = 0
    await router.websocket_disconnect(websocket, data)
    # await live_register.remove(websocket)
    return websocket._ok


typemap = generate_typemap()
