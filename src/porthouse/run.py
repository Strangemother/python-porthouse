"""Run the frontend ingress. FastAPI WebSocket and HTTP on uvicorn.

    py run.py

This starts a new server and loads the `ingress` app.

    run -> ingress -> ...

---

Functionally this simply _runs `uvicorn`_ without the config overhead. All options
are applied within the arguments
"""
import asyncio
from pathlib import Path

import uvicorn

from . import config as conf_module
from .arguments import uvicorn_conf
from .primary import router
from .ingress import app
from . import arguments


HERE = Path(__file__).parent.as_posix()


def async_server(**kw):
    debug = kw.pop('debug', False)
    asyncio.run(main(**kw), debug=debug)


async def main(**kw):
    """
    python -m uvicorn ingress:app --host 127.0.0.1 --port 9004  --reload
    """
    print(kw)
    await router.set_system_config(kw) # The _raw_ config,
    config = get_config(kw) # "ingress:app"
    # config = get_config(app, kw) # "ingress:app"
    task = await start_server_task(config)
    # return await run_default_server(config)
    ## Ensure to wait for the task.
    await task


def get_config(config=None):
    """Given a target app, Create and return a uvicorn Config object.

        get_config()

    The real source: site-packages/uvicorn/config.py
    """
    _conf = config or {}
    defaults = dict(host=conf_module.HOST,
            port=conf_module.PORT,
            log_level=conf_module.LOG_LEVEL,
            reload=conf_module.RELOAD,
            reload_dirs=[HERE],
            use_colors=False,
            ws_max_size=conf_module.WS_MAX_SIZE,
            target=conf_module.INGRESS_APP,
        )

    arg_items = arguments.get_parsed_args().items()
    wanted = tuple(uvicorn_conf.UVICORN_CONF_ALLOWED.keys()) + ('target',)
    defaults.update({x:y for x,y in _conf.items() if x in wanted})
    # defaults.update(_conf)
    print(defaults)
    target = defaults.pop('target')
    c = uvicorn.Config(target, **defaults)
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

