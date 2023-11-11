
import asyncio
import uvicorn
from fastapi import FastAPI
from pathlib import Path

import config as conf

HERE = Path(__file__).parent.as_posix()

from ingress import app, router

async def main():
    """
    python -m uvicorn ingress:app --host 127.0.0.1 --port 9004  --reload
    """
    config = uvicorn.Config(app, # "ingress:app",
            host=conf.HOST,
            port=conf.PORT,
            log_level="info",
            reload=conf.RELOAD,
            reload_dirs=[HERE],
            use_colors=False,
            )

    return await run_config(config)
    # return await run_default_server(config)


async def run_default_server(config):
    server = uvicorn.Server(config)
    await server.serve()


async def run_config(config):
    server = uvicorn.Server(config)
    task = asyncio.create_task(server.serve())

    names = await get_socket_names(server)

    conf.ADDRESSES = names
    # await app.set_socket_addresses(names)
    await router.set_primary_sockets(names)

    await task


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
    asyncio.run(main(), debug=True)

