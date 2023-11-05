# Server, Router, Ingress

Porthouse is segemented by task within the server itself.


## Server

The server hosts the ingress and a router, accepting messages and posting them locally. The server itself can have its own pipes to other servers. These act as balancing and messaging routes.

Server connections have special permissions not usually assigned to clients. They can receive all messages from another server and act like a standard pipe or tcp connection.

The server can be considered as the web-service for porthouse.


## Ingress

The face of the server, accepting clients through websockets or other formats - such as udp, tcp,

The ingress can be anything you can handle, ensuring to _accept_ your client and receive messages. For example a local app may have a bluetooth protocol, ingressing driver function reads.

The messages are binary or text, sent into the Router


## Router

The router accepts the message and the owning socketid. The socket ID is the identifier to the services allowed. The socket is configured by a Client reference.

The router accepts the message, discovers expecting sockets by passing the message through steps of routing; through rooms, potentially hops, resolving sockets. The socket receives the message from the router.

The messages appears at the other end as a functional call, perhaps to the same router - however the message may have been dispatched through a server pipe to another server.

