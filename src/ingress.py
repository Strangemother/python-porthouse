from fastapi import WebSocket, FastAPI
from fastapi import Request

from loguru import logger
dlog = logger.debug

HOST = '127.0.0.1'
DEBUG = True


app = FastAPI(host=HOST, debug=DEBUG)


@app.on_event("startup")
async def startup_event():
    """Run the host manager within the async for await tools"""
    # await manager.mount()
    dlog('Startup')


import index_page
index_page.mount_jinja_home(app, index_template='index.html')


@app.websocket("/")
@app.websocket("/{token}")
async def websocket_endpoint_primary(websocket: WebSocket,
        token=None):
    dlog('Websocket on primary port.')
    await primary_ingress(websocket, token=token)


from router import Router

router = Router()

# from register import live_register


async def primary_ingress(websocket, **kw):
    """Run an install on an incoming socket.
    """

    websocket._ok = await router.websocket_accept(websocket, **kw)

    while websocket._ok:
        data = await websocket.receive()

        if data['type'] == 'websocket.disconnect':
            ## Return release the socket.
            websocket._ok = 0
            # await websocket.close()
            await router.websocket_disconnect(websocket, data)
            # await live_register.remove(websocket)
            return

        receipt = await router.recv_socket_event(websocket, data)
        # 'send', 'send_bytes', 'send_json', 'send_text',
        if receipt is not None:
            await websocket.send_text(receipt)

