
__all__ = ['StarletteAdapter']

from .base import Adapter, add_adapter


class StarletteAdapter(Adapter):

    def __init__(self, router):
        super().__init__(router)
        self.typemap = self.generate_typemap()

    def generate_typemap(self):
        """Return a dict to map actions to methods. The key should be data['type']
        If the data[type] is not mapped within this dict
        """
        return {
            'websocket.disconnect': self.websocket_disconnect,
            'default': self.default_action,
        }

    async def handle_command_message(self, websocket, data):
        """A Message as a _command_ for the router state. This socket
        may also accept command events.
        """
        return await self.handle_message(websocket, data, default=self.recv_socket_command)

    async def recv_socket_command(self, websocket, data):
        """The function to handle a socket message from the admin ingress.
        This should route with a flag for allowing changes.
        """
        receipt = await self.router.recv_socket_event(websocket, data)
        # 'send', 'send_bytes', 'send_json', 'send_text',
        if receipt is not None:
            # primarily JSON for now.
            await websocket.send_json({'receipt': receipt})
        return 1

    async def handle_message(self, websocket, data, default=None):
        """Given a socket and the new message, read the `type` of message
        and call the `typemap` handler function. If no function is found use
        the `default_action` function.
        If the result from the action method is not a truthy, the socket will
        disconnect.

        Return an `ok` truthy. `0` for _not ok_, `1` for okay.
        """
        if default is None:
            default = self.typemap['default']
        action_func = self.typemap.get(data['type'], None) or default
        ok = await action_func(websocket, data)
        return ok

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

    async def websocket_disconnect(self, websocket, data):
        """Handle the "websocket.disconnect" event from the primary ingress.
        Call upon the router websocket_disconnect method and flag the websocket as
        not _ok_.
        """
        websocket._ok = 0
        await self.router.websocket_disconnect(websocket, data)
        # await live_register.remove(websocket)
        return websocket._ok


add_adapter('starlette', StarletteAdapter)
