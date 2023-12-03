"""The adapter provides a facade between the ingress and the router, hoisted by
the primary. This allows inbound sockets from alterntive libraries to be called
upon correctly. For example Starlette and Sanic use slightly different
terminology to wait upon messages + Sanic does not expose the socket `accept()`.
"""

__all__ = ['add_adapter', 'get_adapter', 'Adapter']

ADAPTERS = {
    '_cache': {}
}


def add_adapter(name, class_):
    ADAPTERS[name] = class_


def get_adapter(name, router):
    inner_name = f"{name}-{router.uuid}"
    r = ADAPTERS['_cache'].get(inner_name, None)
    if r is None:
        r = ADAPTERS['_cache'][inner_name] = ADAPTERS[name](router)
    return r


class Adapter(object):

    def __init__(self, router):
        self.router = router

    async def websocket_accept(self, websocket, **extras):
        # return await websocket.accept()
        return await self.router.websocket_accept(websocket, **extras)

    async def wait_receive(self, websocket, **extras):
        return await websocket.receive()

    async def wait_receive_json(self, websocket, **extras):
        return await websocket.receive_json()

    async def wait_exit(self, websocket):
        if websocket.client_state.value == 1:  # websocket.CONNECTED
            # await websocket.close()
            await self.close(websocket)

    async def close(self, websocket, **extras):
        await websocket.close()

    def validate_accept(self, websocket, **extras):
        return self.router.access_rules.is_valid(websocket, **extras)

    async def handle_command_message(self, websocket, data):
        """A Message as a _command_ for the router state. This socket
        may also accept command events.
        """
        return await self.handle_message(websocket, data)

    async def handle_message(self, websocket, data):
        """Given a socket and the new message, read the `type` of message
        and call the `typemap` handler function. If no function is found use
        the `default_action` function.
        If the result from the action method is not a truthy, the socket will
        disconnect.

        Return an `ok` truthy. `0` for _not ok_, `1` for okay.
        """
        return await self.default_action(websocket, data)

    async def default_action(self, websocket, data):
        """The default function for an incoming message from a websocket.
        Call to the router recv_socket_event and return a _receipt_ back to the
        client (if given).

        Return `1` or any truthy as an "ok" to _continue listening_.
        """
        receipt = await self.router.recv_socket_event(websocket, data)
        # 'send', 'send_bytes', 'send_json', 'send_text',
        if receipt is not None:
            await websocket.send_text(receipt)
        return 1

