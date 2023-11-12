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


import gc

from collections import defaultdict
import uuid

from . import rooms


CONNECTIONS = {
    'sockets': {},
    '_count': 0,
    '_total': 0
}

class Register(object):

    uuid_param = 'socket_id'

    def get_connections(self):
        return CONNECTIONS['sockets']

    async def add(self, websocket, _uuid):
        # bind client
        _uuid = _uuid or str(uuid.uuid4())
        setattr(websocket, self.uuid_param, _uuid)
        CONNECTIONS['sockets'][_uuid] = websocket
        CONNECTIONS['_count'] += 1
        CONNECTIONS['_total'] += 1
        self.log_count()
        return _uuid

    def log_count(self):
        count = CONNECTIONS['_count']
        l = len(CONNECTIONS['sockets'])
        t = CONNECTIONS['_total']
        dlog(f'Count: {count}, real: {l}, total: {t}')

    async def resolve_sockets(self, names, ignores=None):
        live = CONNECTIONS['sockets']
        ignores = ignores or ()
        res = ()
        for name in names:
            if name in ignores:
                continue
            socket = live.get(name)
            if socket:
                res += (socket,)
        return res

    async def remove(self, websocket, error=None):
        """Called automatically or requested through the API to _disconnect_
        the target websocket by sending a close 1000 event.
        """
        _uuid = getattr(websocket, self.uuid_param)
        dlog(f'drop: {_uuid}')
        sid = CONNECTIONS['sockets'].pop(_uuid, None)

        if sid is not None:
            CONNECTIONS['_count'] -= 1
            self.log_count()
            return _uuid

    def _garbage_collect(self):
        total = CONNECTIONS['_total']
        if total % 100 == 0:
            print('\nCollecting\n')
            gc.collect()  # Force garbage collection
            v = gc.garbage
            dlog(f'garbage {v}')


live_register = Register()