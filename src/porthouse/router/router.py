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
import uuid
import asyncio

from ..log import *
from .. import log

from ..rules import RuleSet, IPAddressRule, TokenRule
from ..register import live_register
from ..envelope import Envelope
from .. import (config as conf,
                 tokens,
                 rooms,
                 backpipe,
                 adapters,)

from .tell import TellCommand
from .methods import Methods


__all__ = ['Router']


from ..dispatch.supercast import supercast as supercast_dispatch_method
from ..dispatch.roomcast import roomcast as roomcast_dispatch_method


class Router(backpipe.BackPipeMixin):
    adapter_class = None
    dispatch_method = 'roomcast'
    name = None
    rooms = None
    command_routers = None
    backpipe_token = None

    def __init__(self, adapter=None, name=None, command_router=None):
        host = f'{conf.HOST}' #:{conf.PORT}'
        self.name = name
        self.uuid = str(uuid.uuid4())

        self.backpipe_token = '4e00a95c-b42d-42ca-9b20-625b6d5f3605'

        self.tell_command = TellCommand()
        self.rooms = rooms.Rooms()
        self.tokens = tokens.Tokens(
                api_endpoint='http://localhost:8000',
                tokenizer_onboarding_token=35289759287529875,
            )

        self.adapter_class = self.resolve_adapter(adapter) if adapter else None
        self.access_rules = RuleSet(
                IPAddressRule(host=host, check_port=False),
                TokenRule(tokens=self.tokens, param='token'),
            )

        self.command_router = command_router
        self.dispatch_methods = {
            'supercast': supercast_dispatch_method,
            'roomcast': roomcast_dispatch_method,
        }

    def __str__(self):
        c = self.__class__.__name__
        m = self.__class__.__module__
        i = self.name or id(self)
        return f'<{m}.{c} "{i}">'

    async def set_system_config(self, namespace_dict):
        """Assign a large config object given from the system at
        setup.
        This is likely called before the server is awake (before the primary
        sockets are applied).

        Produced by converting the namespace and any extended config to a dict.
        """
        k = tuple(namespace_dict.keys())
        log.d(f'apply namespace dict (keys): {k}')
        self._system_config = namespace_dict
        self.prepare_backpipe(ports=namespace_dict.get('balance_ports'))

    async def set_primary_sockets(self, addresses):
        """The _first method_ to run.
        """
        self.primary_addresses = addresses

        my_host, my_port = addresses[0]
        log.d('set_primary_sockets', my_host, my_port)
        if self.has_backpipe:
            await self.start_backpipe(my_host, my_port)

    async def backpipe_recv(self, message, websocket):
        """A message from the _backpipe_.
        """
        log.d(f'RECV: "{message}"')

    async def startup(self, app, adapter):
        """The _first method_ to run.
        """
        log.d(f'mounting to {app=}')
        self.adapter_class = self.resolve_adapter(adapter)
        if self.command_router is not None:
            await self.tell_command.add_command_router(self.command_router, adapter)
            self.command_router = None
        self.can_tokenize = await self.tokens.ask(tokens.tokenizer_onboarding_token)

    def resolve_adapter(self, pointer):
        """If the given pointer is a string, resolve from the
        possible adapters.

        Return a class.
        """
        if isinstance(pointer, str):
            return adapters.get_adapter(pointer, self)
        return pointer

    async def shutdown(self, app):
        """The _first method_ to run.
        """
        print('SHUTDOWN')
        await self._pipe.close()
        # self._pipe = await backpipe.connect(uri)

    async def websocket_can_accept(self, websocket, **extras) -> bool:
        extras.setdefault('uuid', str(uuid.uuid4()))
        accept = await self.access_rules.is_valid(websocket, **extras)
        return accept

    async def websocket_accept(self, websocket, **extras) -> bool:
        log.d(f'Websocket ingress {websocket}')
        _uuid = str(uuid.uuid4())
        extras.setdefault('uuid', _uuid)

        if await self.websocket_can_accept(websocket, **extras) is False:
            return False

        token = extras['token']
        ok = await self.use_token(websocket, _uuid, token)
        if ok is False: return False

        # Ensure to call as fast as possible.
        await websocket.accept()

        accept = await self.websocket_onboard(websocket, _uuid, token)
        # Return the ok. This is `True` to _enable waiting_.
        return accept

    async def websocket_onboard(self, websocket, _uuid, token) -> bool:
        await self.tell_command.connect(websocket, _uuid, token)

        # Bind to the local register
        await live_register.add(websocket, _uuid)

        log.d('Sending backpipe accept statement')
        await self.backpipe_send(f'accepted: {_uuid}')
        # Turn on connections.
        await self.apply_auto_subscribed(websocket, token)
        # Return the ok. This is `True` to _enable waiting_.
        return True

    async def use_token(self, websocket, _uuid, token):
        ok = await self.tokens.use_token(_uuid, token)
        if ok is False:
            log.d('tokens.use_token failed.')
            return False
        websocket.token = token

    async def apply_auto_subscribed(self, websocket, token):
        """Suscribe this socket to the allowed (auto) rooms given the token
        as a binding key.

        """
        # if auto_subscribe, bind to rooms.
        obj = await self.tokens.get_token_object(token)
        if obj.get('auto_subscribe', False) is True:
            print(f'\nApplying Auto subscriptions to {token=}\n')
            subscribed = await self.get_socket_subscriptions(websocket)
            print(f'\nto {subscribed=}\n')
            await self.bind_socket_rooms(websocket, subscribed)
        else:
            log.d('auto_subscribe is False')

    async def recv_socket_event(self, websocket, data):
        """The recv_socket_event method is the primary method for the
        ingress, called when a (exterior) waiting socket dispatches data.

        Wrap the data into an Envelope and call `dispatch()`
        """
        log.d(f'Data {data}')
        msg = Envelope(data, websocket)
        await self.dispatch(websocket, msg)
        return msg.id

    async def websocket_disconnect(self, websocket, data):
        """Called by the ingress, the websocket_disconnect method detaches
        the socket from all internal graphs and removes one active token use.
        """
        log.d('disconnect')
        # Tell the client pipe
        sid = websocket.socket_id
        await self.rooms.remove_connection(sid)
        await live_register.remove(websocket)
        await self.tell_command.disconnect(websocket, websocket.token, data)
        await self.tokens.unuse_token(sid, websocket.token)#, extras['token'])

    async def dispatch(self, websocket, msg:Envelope):

        method = roomcast_dispatch_method

        if self.dispatch_method == Methods.SUPERCAST:
            method = supercast_dispatch_method

        method = self.dispatch_methods.get(self.dispatch_method) or None
        if method:
            return await method(self, websocket, msg)
        return self.no_dispatch(websocket, msg)

    async def no_dispatch(self, websocket, msg):
        """The given message does not have a valid dispatch method.
        This occurs if the `self.dispatch_method` is not within the avaiable
        `self.dispatch_methods` list.
        """
        log.e(f'Lost Message due to no valid dispatch method, {msg.id}')
        log.d(f'Origin: {websocket=}')

    async def filter_allowed_destinations(self, websocket, msg):
        names = msg.destination or ()
        ## If names is None, assume all subscribed
        subscribed = await self.get_socket_subscriptions(websocket)
        allowed = subscribed

        if len(names) > 0:
            log.d('Filtering destination names')
            # if names, but is not subscribed; reject
            ## Filter to live sockets.
            allowed = tuple(set(subscribed) & set(names))
        return allowed

    async def bind_socket_rooms(self, websocket, room_names):
        # Apply the socket to the room connection (if allowed)
        log.d(f'Auto Binding websocket to {room_names}')
        for name in room_names:
            room = self.rooms.get_room(name)
            if room is None:
                continue
            await room.add_connection(websocket)

    async def send_to(self, sockets, origin_socket, msg:Envelope):
        for socket in sockets:
            await socket.send_text(msg.content['text'])
        return sockets

    async def gather_sockets(self, *room_names, origin_socket=None):
        # For each room, collect the connected
        # sockets.
        res = ()
        for room in room_names:
            res += await self.resolve_sockets(room, origin_socket)
        return res

    async def resolve_sockets(self, room_name, origin_socket=None):
        """Return all the live sockets for the given room name
        """
        live = self.rooms.get_room(room_name).connections
        ignores = (origin_socket,) if origin_socket else ()
        return await live_register.resolve_sockets(live, ignores)

    async def get_socket_subscriptions(self, websocket):
        token = websocket.token
        return await self.get_token_subscriptions(token)

    async def get_token_subscriptions(self, token):
        """Return a list of rooms and clients this socket is subscribed to.
        """
        token_obj = await self.tokens.get_token_object(token)
        subscriptions = token_obj.get('subscriptions', None)
        if subscriptions is None:
            if token_obj.get('inherit_subscriptions', False):
                owner = await self.get_token_owner(token_obj)
                subscriptions = owner.get('subscriptions')

        return tuple((subscriptions or {}).keys())

    async def get_token_owner(self, token):
        return await self.tokens.get_owner(token)


