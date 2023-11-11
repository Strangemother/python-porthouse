# Server, Router, Ingress


One of the key design philosophies in our system is the fundamental decoupling of the ingress server from the router. This architecture choice ensures flexibility and scalability. It allows for the integration of alternative ingress points, potentially built with different frameworks or designed to handle other types of sockets.

These alternative ingresses can seamlessly loop into and send messages to the same router, maintaining system consistency while expanding our capacity to handle diverse types of traffic and connections.


## Server

The server hosts the ingress and a router, accepting messages and posting them locally. The server itself can have its own pipes to other servers. These act as balancing and messaging routes.

Server connections have special permissions not usually assigned to clients. They can receive all messages from another server and act like a standard pipe or tcp connection.

The server can be considered as the web-service for porthouse.


## Ingress

- Acts as the main entry point for all external connections.
- Handles both HTTP and WebSocket requests.

The face of the server, accepting clients through websockets or other formats - such as udp, tcp,

The ingress can be anything you can handle, ensuring to _accept_ your client and receive messages. For example a local app may have a bluetooth protocol, ingressing driver function reads.

The messages are binary or text, sent into the Router


## Router

The router accepts the message and the owning socketid. The socket ID is the identifier to the services allowed. The socket is configured by a Client reference.

The router accepts the message, discovers expecting sockets by passing the message through steps of routing; through rooms, potentially hops, resolving sockets. The socket receives the message from the router.

The messages appears at the other end as a functional call, perhaps to the same router - however the message may have been dispatched through a server pipe to another server.


### Message Handling
- Minimally manipulates incoming messages.
- Wraps messages in an envelope.
- Routes messages through "rooms" (similar to WebSocket channels).
- Can present messages to connected sockets within rooms or pass them to other rooms.

## `router.recv_socket_event` Function

### Functionality
- Activates when data is sent to the server via a WebSocket.
- Wraps incoming data in an envelope.
- Passes data to the router for distribution.

## Asynchronous Processing

- Ensures unique handling of each message, avoiding conflicts.
- Handles messages asynchronously, allowing for efficient processing without data conflicts or concurrency issues.
