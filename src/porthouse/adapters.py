"""The adapter provides a facade between the ingress and the router, hoisted by
the primary. This allows inbound sockets from alterntive libraries to be called
upon correctly. For example Starlette and Sanic use slightly different
terminology to wait upon messages + Sanic does not expose the socket `accept()`.
"""


ADAPTERS = {
    '_cache': {}
}


def add_adapter(name, class_):
    ADAPTERS[name] = class_


def get_adapter(name, router):
    r = ADAPTERS['_cache'].get(name, None)
    if r is None:
        r = ADAPTERS['_cache'][name] = ADAPTERS[name](router)
    return r

class Adapter(object):

    def __init__(self, router):
        self.router = router

    async def accept(self, websocket, **extras):
        return await websocket.accept()

    async def wait_receive(self, websocket, **extras):
        return await websocket.receive()

    async def close(self, websocket, **extras):
        await websocket.close()

    def validate_accept(self, websocket, **extras):
        return self.router.access_rules.is_valid(websocket, **extras)


class StarletteAdapter(Adapter):
    pass


add_adapter('starlette', StarletteAdapter)