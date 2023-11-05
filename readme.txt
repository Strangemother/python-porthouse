A simplification of `socket_server` and `websocket`.

All sockets have a 'state' bound through a pipe from a state machine
A client id is random, assigned to the correct procedure through parent ownership
A parent ownership must register the
    path
    token
    client id
    ...
An auth endpoint after the client has accepted, tests the users aithenticity

channels, rooms and lobbies are graph bindings to messaging functions.

A message is packaged from the ingress into the mesh,
The mesh distributes thepacets to the correct channel.

## routine

A single node will need to receive and continue messages as they persist through the graph. This acts as a broadcast to other nodes.
A reverse path identity is applied on the edges. When a node mounts to the mesh, the id bubbles  through to another nodes. The id on edge reference allows message passing though to the correct edge  when a message is routed.

An ingress message serves as a wrapper, testing the message for early types. Then the message is 'routed'. This involves checking the client ID of the message and sending to its pipes.


---

A message appears through the ingress, and dropped into the loop.
The message is wrapped and tested for a flow


A process flow for a complex setup of a socket:

    pre-auth: header tests for standard connections
    auth: client id and user tokens
    message cycle: send a message to waiting rooms

The auth step determines who owns a socket, and its capabilities - such as _room lock_ or the ability to step owned rooms.

## Client Class

The client class wraps a socket, persistent meta data (such as the owner), session meta data (such as the current channels)


