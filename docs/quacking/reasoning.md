# Reasoning Examples

Some examples to factor how the platform is written

## Double Sockets

Signalling connections or 'double sockets' allow a connection coupled with a relative to define extra commands on the original socket.

For example if we have a socket stream of bytes, of which will stop in X seconds, the
signalling socket will announce a change a JSON message, without interrupting the original stream.

For Duplex commands; such as FTP - you can push content through the primary socket, and receive logs through the second.

---

Debug and command channels.

The command channel can tell the client how to interact with the server. A debug channel can receive errors down the pipe, not usually applied to the user, such as "disconnected"


## Offset Messaging

The message to receiver routing should occur complete off the websocket tooling. fundamentally the websocket is one input method to the messaging machine.

The rooms connections, subscribing, and routing occurs within the independent tool.


## Input Methods

The primary input method is _messages_ through websocket sockets. However a _client_ can access their mesh through and protocol. The client should be able to parse sent and received messages, the piping through the middle is done through porthouse.

The input methods input:

+ Websocket
+ Webpage (form POST)
+ UDP/TCP
+ FTP

Functionally the client performs a `send()` through their client. The ingress may be a UDP or another communication type. The ingress receives a UDP, and transmits across the already bridged interface.


## Senior Bridge

An Ingress server is a server accepting client connections through the expected protocol. However it may just be a _dump client_ and pass the messages to the bridge in the form of websocket or TCP.

This is an independent 'meshing' socket bound as a large duplex pipe to another meshing ingress client. Two ingress clients connected may message each-other privately - potentially on a higher throughput connection.


