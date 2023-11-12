"""Ingress

The ingress is the externally accessible frontend for the incoming connections.
"""
import asyncio
from contextlib import asynccontextmanager

from fastapi import WebSocket, FastAPI
from fastapi import Request

from loguru import logger
dlog = logger.debug

from . import config as conf
from . import index_page
from . import primary


app = FastAPI(host=conf.HOST, debug=conf.DEBUG, lifespan=primary.lifespan)

index_page.mount_jinja_home(app, index_template='index.html')


@app.websocket("/")
@app.websocket("/{token}")
async def websocket_endpoint_primary(websocket: WebSocket,token=None):
    dlog('Websocket on primary port.')
    await primary.primary_ingress(websocket, token=token)
