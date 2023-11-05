# Messages Inbound

A message is binary or text and bound to a socket id.

The message is send to any subscribed environments. The message is considered 'raw'
and is wrapped by a Envelope class. The envelope can be altered and meta marked
by the messaging system, but in most cases the root message doesn't change.

A message has:

    MessageID: auto generated
    Client ID: Given
    Socket ID: auto generated
    Message
    ...

This is in the raw form from the socket.

The message system (from know on the router) will read the socket id, find the target client or room, (or all current connected), collapse to sockets, and run 'recv' on every socket.

The receiver socket may be another socket channel - where the message will leave this router into, into another.

The router or room may have a primary pipe, sending the information to another assigned server.

## Hops

An envelope can register _hops_. Each hop is a server and socket. The hop count and path can define the distance from the origin.