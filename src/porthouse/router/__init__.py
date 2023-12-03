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

from .command import *
from .router import *
from .tell import *