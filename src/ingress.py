# import sys
# from pathlib import Path
# from typing import List


# from porthouse import WebSocket
from fastapi import WebSocket, FastAPI
from fastapi import Request

HOST = '127.0.0.1'
DEBUG = True


app = FastAPI(host=HOST, debug=DEBUG)

# import base
# base.mount_jinja_home(app, index_template='index_orig.html')


# import asyncio

# async def slow_loop():
#     while 1:
#         print('slow_loop')
#         await asyncio.sleep(1)

# async def other_loop():
#     while 1:
#         print('other_loop')
#         await asyncio.sleep(1.2)


# loop = asyncio.get_event_loop()
# cors = asyncio.wait([slow_loop(), other_loop()])
# # loop.run_until_complete(cors)

from fastapi.responses import HTMLResponse
from typing import Optional
from jinja2 import Template


@app.on_event("startup")
async def startup_event():
    """Run the host manager within the async for await tools"""
    # await manager.mount()
    print('Startup')


import index_page
index_page.mount_jinja_home(app, index_template='index.html')

# @app.get("/", response_class=HTMLResponse)
# async def jinja_home_callback(request: Request, id: Optional[str]=None):
#     index_template = 'index.html'
#     templ = Template(index_template)
#     d = {"request": request, "id": id}
#     return templ.render(d)


# @app.websocket("/{token}/{channel}")
@app.websocket("/")
@app.websocket("/{token}")
async def websocket_endpoint_primary(websocket: WebSocket,
        token=None):
    print('Websocket on primary port.')
    await primary_ingress(websocket, token=token)


async def primary_ingress(websocket, **kw):
    """Run an install on an incoming socket.
    """
    print('Websocket ingress', websocket)
    await websocket.accept()
    websocket._ok = 1

    while websocket._ok:
        data = await websocket.receive()
        print('Data', data)
        if data['type'] == 'websocket.disconnect':
            ## Return release the socket.
            websocket._ok = 0
            # await websocket.close()
            return

        # 'send', 'send_bytes', 'send_json', 'send_text',
        await websocket.send_text('Accepted')

