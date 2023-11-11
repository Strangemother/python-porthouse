import asyncio
from contextlib import asynccontextmanager

from fastapi import WebSocket, FastAPI
from fastapi import Request

from loguru import logger
dlog = logger.debug

import config as conf
from router import Router
import index_page

router = Router()


@asynccontextmanager
async def lifespan(app: FastAPI):
    dlog('lifespan Startup')
    # await asyncio.sleep(3)
    # dlog('lifespan Startup - mount')
    await router.startup(app)
    yield
    dlog('lifespan shutdown')
    await router.shutdown(app)


app = FastAPI(host=conf.HOST, debug=conf.DEBUG, lifespan=lifespan)

index_page.mount_jinja_home(app, index_template='index.html')


@app.websocket("/")
@app.websocket("/{token}")
async def websocket_endpoint_primary(websocket: WebSocket,
        token=None):
    dlog('Websocket on primary port.')
    await primary_ingress(websocket, token=token)

# from register import live_register

async def default_action(websocket, data):

    receipt = await router.recv_socket_event(websocket, data)
    # 'send', 'send_bytes', 'send_json', 'send_text',
    if receipt is not None:
        await websocket.send_text(receipt)

    return 1


async def websocket_disconnect(websocket, data):

    websocket._ok = 0
    await router.websocket_disconnect(websocket, data)
    # await live_register.remove(websocket)
    return


type_map = {
    'websocket.disconnect': websocket_disconnect
}


async def primary_ingress(websocket, **kw):
    """Run an install on an incoming socket.
    """
    websocket._ok = await router.websocket_accept(websocket, **kw)

    while websocket._ok:
        data = await websocket.receive()
        func = type_map.get(data['type'], default_action)
        ok = await func(websocket, data)

        # if data['type'] == 'websocket.disconnect':
        #     websocket._ok = 0
        #     await router.websocket_disconnect(websocket, data)
        #     # await live_register.remove(websocket)
        #     return

        # receipt = await router.recv_socket_event(websocket, data)
        # # 'send', 'send_bytes', 'send_json', 'send_text',
        # if receipt is not None:
        #     await websocket.send_text(receipt)
    # else:
    #     await websocket.close()

