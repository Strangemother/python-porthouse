"""Run the frontend ingress. FastAPI WebSocket and HTTP on uvicorn.

    py run.py

"""
import asyncio
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from . import config as conf_module
from .ingress import app
from .primary import router

HERE = Path(__file__).parent.as_posix()


def async_server(**kw):
    debug = kw.pop('debug', False)
    asyncio.run(main(**kw), debug=debug)


async def main(**kw):
    """
    python -m uvicorn ingress:app --host 127.0.0.1 --port 9004  --reload
    """
    config = get_config(app, kw) # "ingress:app"
    task = await start_server_task(config)
    # return await run_default_server(config)
    ## Ensure to wait for the task.
    await task


def get_config(target, config=None):
    """Given a target app, Create and return a uvicorn Config object.

        get_config()

    The real source: site-packages/uvicorn/config.py
    """
    _conf = config or {}
    new_conf = dict(host=conf_module.HOST,
            port=conf_module.PORT,
            log_level="info",
            reload=conf_module.RELOAD,
            reload_dirs=[HERE],
            use_colors=False,
            ws_max_size=conf_module.WS_MAX_SIZE,
        )
    new_conf.update(_conf)
    c = uvicorn.Config(target, **new_conf)
    return c


async def run_default_server(config):
    """Run a uvicorn server in the default manner, without the
    task offset and port capture of `start_server_task`

    Return None
    """
    server = uvicorn.Server(config)
    await server.serve()


async def start_server_task(config):
    """Create the server and install it as an async task
    Wait for the server to _start_ then inspect for the
    open socket addresses. Finally call upon the router to
    set the new socket names.

    Return the server task cooroutine
    """
    server = uvicorn.Server(config)
    # await router.prepare_backpipe()
    task = asyncio.create_task(server.serve())
    ## To capture the used ports we wait for the
    # server.servers[].started, then grab those.
    # As the task is already running, this is non-blocking.
    names = await get_socket_names(server)

    conf_module.ADDRESSES = names

    ## Tell the router its addresses (usually 1 pair)
    await router.set_primary_sockets(names)
    # await app.set_socket_addresses(names)
    return task


async def get_socket_names(server):
    """Return a tuple of tuples, for the server socket
    addresses of the running server.
    If the server is not `started`, async wait until the
    server has started and containing the server socket data.

        (
            ('127.0.0.1', 9002,)
        )

    Returns a tuple of tuples
    """
    while not server.started:
        await asyncio.sleep(0.1)

    names = ()
    for server in server.servers:
        for socket in server.sockets:
            names += (socket.getsockname(), )

    return names


if __name__ == "__main__":
    async_server(debug=True)

