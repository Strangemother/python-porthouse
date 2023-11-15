# Porthouse Service (Rename In Progress)

The Porthouse Service provides a storage and request point for room, users, tokens and other persistent information. This is useful to configure a porthouse using a UI.

---


## Events

Events of the UI should emit into the mesh, and visa-versa. A router may access the service as needed to refresh information, and changes within the service should immediately propagate across the mesh; such as room subscriptions and socket drops.

This requires a connection of the _UI_ service to the router, primarily through websockets.

Two _throughputs_ may communicate to the mesh, from the back of the UI service, or through a socket in the users interface.


## Service BackPipe

A _Backpipe_ is a persistent socket binding routers. It allows cross router communication through an _always-on_ socket outside of the client socket stack.

A Service has a similar connection, bound _behind_ the UI as part of the server source. This allows the website server (UI Service) to transmit changes on an independent line without using the user as a proxy.


## Owner Pipe

The porthouse defines a distinction between _client_ sockets and _owner_ sockets. Each may bind to the router mesh and accept distinct messages. For example "debug" messages through the owner pipe, but not to clients.

This is a special connection allowing the _owner_ to collect a wholesome view of all their sockets, events, and any mesh changes on their own primary channel.

This isn't a _double pipe_ (where a client has two pipes, likely for a binary/event stream pair), instead this is a _level 1_ pipe, allowing visibility over the whole mesh and anything pertaining to the owner.

