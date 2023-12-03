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
# import uuid
# import asyncio



# from .rules import RuleSet, IPAddressRule, TokenRule
# from .register import live_register
from ..envelope import Envelope
# from . import config as conf
from .. import log
from .. import tokens
from .router import Router
# from . import rooms
# from . import backpipe
# from . import adapters

__all__ = ['CommandRouter']


class CommandRouter(Router):
    """A CommandRouter is a router designed to ferry messages through the command
    mesh, to owners regarding a primary router.
    In cases such as _connect_ and _disconnect_, the owner receives messages
    through their command pipe.

    This is functionally designed to be somewhat separate from the primary meshing
    allowing routing without accidental crossover to other meshes.
    """
    assigned = None

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.assigned = ()

    async def tell_assigned(self, assigned, adapter=None):
        """A router assignment occured on the bound router. This may be _this_
        router, as the first binding of the child.
        """
        log.d(f'Assigned {assigned}')
        self.assigned += (assigned, )
        await self.startup(None, adapter)

    async def tell_disconnect(self, websocket, _uuid, data):
        log.d(f'...tell owners about disconnect ID: "{websocket.socket_id}"')
        message = f"disconnected: {_uuid}"
        token = websocket.token
        await self.message_out(websocket, message, token, _uuid)


    async def tell_connect(self, websocket, _uuid, token):
        """The websocket has connected and onboarded to the mesh. The next stage
        is integrating to the live wire.

        Tell the owner of the socket (using the token), this _uuid has connected.
        The owner may use this _uuid as a control id.
        """
        message = f"connected: {_uuid}"
        return await self.message_out(websocket, message, token, _uuid)

    async def message_out(self, websocket, message, token, origin_socket=None):
        # 1. get owner
        owner = await self.get_token_owner(token)
        # 2. filter connects
        room = self.get_owner_room(owner)
        allowed = (room, )
        # Convert the room names to live sockets.
        sockets = await self.gather_sockets(*allowed, origin_socket=origin_socket)
        log.d(f'{len(sockets)} target sockets')
        # 3. envelope
        msg = Envelope.wrap(message, websocket)
        # 4. dispatch
        return await self.send_to(sockets, websocket, msg)
        # 5. receipt?

    async def apply_auto_subscribed(self, websocket, token):
        """On the command channel a user will auto subscribe to their one room.
        (This is given they're auth'd correctly).
        """
        # if auto_subscribe, bind to rooms.
        # obj = await self.tokens.get_token_object(token)
        subscribed = await self.get_token_subscriptions(token)
        log.d(f'{subscribed=}')
        await self.bind_socket_rooms(websocket, subscribed)

    async def get_token_subscriptions(self, token):
        """Currently, for the command channel - a token owned by user may only enter
        their singular freeport.
        Therefore each user has one _room_ all messages are sent into.
        """
        token_obj = await self.tokens.get_token_object(token)
        owner = await self.get_token_owner(token)
        log.d(f'Token {owner=}')
        return (self.get_owner_room(owner),)

    def get_owner_room(self, owner):
        return owner['username']
