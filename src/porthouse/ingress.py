"""Ingress

The ingress is the externally accessible frontend for the incoming connections,
initiated or called upon by a runner such as uvicorn.

    run -> ingress -> primary -> ...
"""
import asyncio
from contextlib import asynccontextmanager

from fastapi import WebSocket, FastAPI
from fastapi import Request

from . import config as conf
from . import index_page
from . import primary
from . import log

app = FastAPI(host=conf.HOST, debug=conf.DEBUG, lifespan=primary.lifespan)

index_page.mount_jinja_home(app, index_template='index.html')


@app.websocket("/")
@app.websocket("/{token}")
async def websocket_endpoint_primary(websocket: WebSocket,token=None):
    log.d('Websocket on primary port.')
    await primary.primary_ingress(websocket, token=token)


@app.websocket("/commander/{token}")
async def websocket_endpoint_commander(websocket: WebSocket,token=None):
    log.d('Websocket on commander port.')
    await primary.command_ingress(websocket, token=token)


from fastapi.responses import RedirectResponse

@app.get("/redirect")
@app.get("/redirect/{token}")
async def redirect_typer(websocket: WebSocket, token=None):
    u = "/"
    if token is not None:
        u = f"/{token}/"
    return RedirectResponse(u)