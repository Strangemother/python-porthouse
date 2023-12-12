
## Offset Messaging

The message to receiver routing should occur complete off the websocket tooling. fundamentally the websocket is one input method to the messaging machine.

The rooms connections, subscribing, and routing occurs within the independent tool.

---

This is done through unique socket ids. Every socket has a very unique id, for a unique client.

A client sends a message through a chosen socket. This is received through the ingress and given to the router.

The router recieves a message, envelopes it, and ferrys to the 'room'. The room has connected sockets. Each socket receives the envelope

The primary ingress generally will use one function; `ingress_recv`

---

subscriptions occur internally. the extern system (the ingress) may query for concurrent subscriptions, but the router manages them.

---

room locking occurs within the router. A message _in_ is effectively black-hole. Messages _out_ to the same socket state stateless for the router, the client and routing machine take account of where the message came from, and what to do with the message data.

    Message in -> [Router] -> (to) -> socket
                                      socket

---

Message data is inspected if the protocol requires it (consider a text-only protocol with a SUBSCRIBE) key message

However if the socket is setup to only send and read pipe information, these message events must be sent in parallel, through the double socket or doule messaging.


## Remote Balancing

A message may need to route through a primary pipe to other servers, therefore all server routers connected on the mesh may need a copy of the meshing. The mesh will balance through the primary pipe:

    router1 add room apples
    router1 connect client 123 apples


