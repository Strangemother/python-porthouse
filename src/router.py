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

from envelope import Envelope
from register import live_register
from rules import RuleSet, IPAddressRule, TokenRule

import config as conf

class Router(object):
    def __init__(self):
        host = f'{conf.HOST}:{conf.PORT}'
        self.access_rules = RuleSet(
                IPAddressRule(host=host),
                TokenRule(param='token'),
            )

    async def websocket_accept(self, websocket, **extras):
        dlog(f'Websocket ingress {websocket}')

        accept = self.access_rules.is_valid(websocket, **extras)

        if accept:
            await websocket.accept()
            uuid = await live_register.add(websocket)

        return accept

    async def recv_socket_event(self, websocket, data):
        dlog(f'Data {data}')
        # Send data to subscribers.
        msg = Envelope(data, websocket)
        await self.dispatch(websocket, msg)
        return msg.id

    async def websocket_disconnect(self, websocket, data):
        print('disconnect')
        # Tell the client pipe
        await live_register.remove(websocket)

    async def dispatch(self, websocket, msg:Envelope):
        # Pluck rooms
        names = msg.destination
        print('Send to', names)
        ## If names is None, assume all subscribed
        # if names, but is not subscribed; reject
        # send to subscribed
        uuid = websocket.socket_id
        # for now, send to all.
        for k, socket in live_register.get_connections().items():
            if k == uuid:
                continue
            await socket.send_text(msg.content['text'])

