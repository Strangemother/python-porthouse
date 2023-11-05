## Clients and Sockets

A Client is a 'user' record bound to permissions, such as _can open connections_
A Socket is a single connect bound to the mesh

A Client connects to the mesh through a socket. A Client may own more than one open socket (consider a single user opening two connections with the same credentials in the same session)

A socket must have a client - the owner of a socket.

When a socket connects it's bound to a client.
A client can be authenticated after the socket connects (considering websocket.open, then authing the connection)

The client is unique to the user, and the general system. The socket is unique to the user client.

When connections and subscriptions are made, they're actioned against the socket (considering two connection from the same session, with unique subscriptions) However the client owning both sockets can see the changes occur on their primary channel.

This means for two sockets a client may have 5 _connections_

    client channel
    socket A
        primary
        debug
    socket B
        primary
        debug

By default a public user do not gain a debug channel.

The service will record ids in a tree - something like:

    client
        socket
            room
        socket
            room
            room

When a socket sends a message it heads directly to the room.
All sockets within the same room gain the message.


