"""The router recieves messages from an ingress
and pipes them to the correct socket (by name) through
a series of hops on a graph.

The steps may be blocks and or rerouted by the rooms.
The router may communicate out to other router.
The router balances its knowledge
and has a record of sockets.

digest message
envelope
return receipt
route to room/client
    room rules
pop to socket, or to void.

The goal is to simple ensure messages are sent to
one or more subscribers, through room association or
targeted addresses.

The outer shell manages throughput to other routers.
"""

from loguru import logger
dlog = logger.debug
elog = logger.error

__all__ = ['TellCommand']

class TellCommand(object):
    """A router dispatches _tell commands_ to other attached routers; likely a
    command router.
    """
    def __init__(self):
        self.command_routers = ()

    async def disconnect(self, websocket, _uuid, data):
        """
            await self.tell_command.disconnect(websocket, data)
        """
        dlog(f'drop {websocket=}')
        for cr in self.command_routers:
            await cr.tell_disconnect(websocket, _uuid, data)

    async def connect(self, websocket, _uuid, token):
        """A new socket has connected to the router with the ID `_uuid`.
        Tell the owner using the _token_ through the command mesh

            await self.tell_command.connect(websocket, _uuid, token)
        """
        dlog(f'new {websocket=}')
        for cr in self.command_routers:
            await cr.tell_connect(websocket, _uuid, token)

    async def add_command_router(self, command_router, adapter):
        """This method is called by _self_ at the router `startup` event.
        The command router should announce the arrival of this router to
        peers and owners.
        """
        dlog('Adding new command router to self.')
        self.command_routers += (command_router, )
        await command_router.tell_assigned(assigned=self, adapter=adapter)

