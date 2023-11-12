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

from loguru import logger
dlog = logger.debug

from .rules import RuleSet, IPAddressRule, TokenRule
from .register import live_register
from .envelope import Envelope
from . import config as conf
from . import tokens
from . import rooms
from . import backpipe


class Router(backpipe.BackPipeMixin):

    def __init__(self):
        host = f'{conf.HOST}' #:{conf.PORT}'

        self.access_rules = RuleSet(
                IPAddressRule(host=host, check_port=False),
                TokenRule(param='token'),
            )
        self.prepare_backpipe()

    async def set_primary_sockets(self, addresses):
        """The _first method_ to run.
        """
        self.primary_addresses = addresses

        my_host, my_port = addresses[0]
        print('set_primary_sockets', my_host, my_port)
        if self.has_backpipe:
            await self.start_backpipe(my_host, my_port)

    async def backpipe_recv(self, message):
        dlog(f'RECV: "{message}"')

    async def startup(self, app):
        """The _first method_ to run.
        """
        print('MOUNT')

    async def shutdown(self, app):
        """The _first method_ to run.
        """
        print('SHUTDOWN')
        await self._pipe.close()
        # self._pipe = await backpipe.connect(uri)

    async def websocket_accept(self, websocket, **extras):
        dlog(f'Websocket ingress {websocket}')
        _uuid = str(uuid.uuid4())
        extras.setdefault('uuid', _uuid)

        accept = self.access_rules.is_valid(websocket, **extras)

        if accept is False:
            return accept

        token = extras['token']
        ok = tokens.use_token(_uuid, token)
        if ok is False:
            dlog('tokens.use_token failed.')
            return False

        websocket.token = token
        # Ensure to call as fast as possible.
        await websocket.accept()
        # Bind to the local register
        await live_register.add(websocket, _uuid)

        dlog('Sending backpipe accept statement')
        await self.backpipe_send(f'accepted: {_uuid}')
        # Turn on connections.
        await self.apply_auto_subscribed(websocket, token)
        # Return the ok. This is `True` to _enable waiting_.
        return accept

    async def apply_auto_subscribed(self, websocket, token):
        # if auto_subscribe, bind to rooms.
        obj = tokens.get_token_object(token)
        if obj.get('auto_subscribe', False) is True:
            subscribed = await self.get_socket_subscriptions(websocket)
            await self.bind_socket_rooms(websocket, subscribed)

    async def recv_socket_event(self, websocket, data):
        """The recv_socket_event method is the primary method for the
        ingress, called when a (exterior) waiting socket dispatches data.

        Wrap the data into an Envelope and call `dispatch()`
        """
        dlog(f'Data {data}')
        msg = Envelope(data, websocket)
        await self.dispatch(websocket, msg)
        return msg.id

    async def websocket_disconnect(self, websocket, data):
        """Called by the ingress, the websocket_disconnect method detaches
        the socket from all internal graphs and removes one active token use.
        """
        dlog('disconnect')
        # Tell the client pipe
        sid = websocket.socket_id
        await rooms.remove_connection(sid)
        await live_register.remove(websocket)
        tokens.unuse_token(sid, websocket.token)#, extras['token'])

    async def dispatch(self, websocket, msg:Envelope):
        # convert the rooms to socket names
        allowed = await self.filter_allowed_destinations(websocket, msg)
        dlog(f'Send to {allowed}')

        # Convert the room names to live sockets.
        sid = websocket.socket_id
        sockets = await self.gather_sockets(*allowed, origin_socket=sid)
        dlog(f'{len(sockets)} target sockets')

        # send to subscribed
        # return await self.supercast(websocket, msg)
        return await self.send_to(sockets, websocket, msg)

    async def filter_allowed_destinations(self, websocket, msg):
        names = msg.destination
        ## If names is None, assume all subscribed
        subscribed = await self.get_socket_subscriptions(websocket)
        allowed = subscribed

        if len(names) > 0:
            dlog('Filtering destination names')
            # if names, but is not subscribed; reject
            ## Filter to live sockets.
            allowed = tuple(set(subscribed) & set(names))
        return allowed

    async def bind_socket_rooms(self, websocket, room_names):
        # Apply the socket to the room connection (if allowed)
        dlog(f'Auto Binding websocket to {room_names}')
        for name in room_names:
            room = rooms.get_room(name)
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
        live = rooms.get_room(room_name).connections
        ignores = (origin_socket,) if origin_socket else ()
        return await live_register.resolve_sockets(live, ignores)

    async def supercast(self, websocket, msg:Envelope):
        uuid = websocket.socket_id
        # for now, send to all.
        for k, socket in live_register.get_connections().items():
            if k == uuid:
                continue
            await socket.send_text(msg.content['text'])

    async def get_socket_subscriptions(self, websocket):
        token = websocket.token
        return await self.get_token_subscriptions(token)

    async def get_token_subscriptions(self, token):
        """Return a list of rooms and clients this socket is subscribed to.
        """
        token_obj = tokens.get_token_object(token)
        subscriptions = token_obj.get('subscriptions', None)
        if subscriptions is None:
            if token_obj.get('inherit_subscriptions', False):
                owner = await self.get_token_owner(token_obj)
                subscriptions = owner.get('subscriptions')

        return tuple((subscriptions or {}).keys())

    async def get_token_owner(self, token):
        return tokens.get_owner(token)
