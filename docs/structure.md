# Structure

    run -> ingress -> primary -> router -> ...

## Run

The `run.py` is the first touch point for starting the app. In CLI form:

    $> porthouse run

The `__main__` offloads to the run. This prepares the configuration for the chosen
server `uvicorn`.


## Ingress

Once the server has started the ingress app is public allowing The app `FastAPI` to accept HTTP and WS requests. The primary goal of the ingress is to collect sockets from the server calls (HTTP requests) and push them into the _primary_. Porthouse is designed to be thinly integrated,
therefore all communication occurs through the `primary`.

An ingress essentially has one functional call `primary_ingress(socket, **extras)`


## Primary

The is designed manage sockets from the ingress, and wait for their messages. All messages are sent to the `router`. This layer cares for the socket, ensuring its _alive_ and pushes messages into the router.

+ Accept Sockets
+ Loop (wait receive)
+ Close Sockets

Consider it the middle-man between "Sockets": the bound connection between client and server, and the "Router": the service passing messages from socket to socket.

When a socket sends a message, it's captured by the primary and sent into the routers primary socket receive function:

```py
receipt = await router.recv_socket_event(websocket, data)
```

The `receipt` is the evidence that _this message_ went into the router. It's the primaries' role to push this down the socket.


## Router

The `router` is essentially the _postman_ for messages from socket to socket. Porthouse is designed to be _function in function out_ where the router tracks a range of sockets (ids), and the primary pushes messages _into_ the router and _forgets_ about it.

The router is designed to pop pushes _out_ to a target list of sockets (IDs), and they happen to be bound to a socket with a `send` method.

The goal is isolated point to point messaging encompassing groups (rooms). The Router wraps the message into an "Envelope" to dispatch it through to the target sockets. The destination of the message may be _local_, or through _hops_. In all cases the router is resolving rooms, and pushing to attached sockets.

In reality, the router is more involved, due to its requirement to track _live sockets_ in rooms. Therefore it needs access to the socket at times and be told when a socket drops. That said, the root functionality is clear:

```py
## From primary
# receipt = await router.recv_socket_event(websocket, data)

msg = Envelope(data, websocket)
await router.dispatch(websocket, msg)
msg.id
```

And routing:

```py
allowed = await self.filter_allowed_destinations(websocket, msg)
sockets = await self.gather_sockets(*allowed)
await self.send_to(sockets, websocket, msg)
```

Gathering allowed destinations (and subsequently sockets) is bound to the
permissions of the given socket. The initial entry (`router.accept`) tested the
socket token and assigned it the correct permissions. This is done through `subscriptions` of `tokens` to `rooms` owned by `clients`.

## Rooms

A `room` defines a group of possible connected clients under a collection defined by the owner client. The tokens are pre-assigned to _rooms_, allowing messaging through those rooms to any client with the token. The owner will setup permissions for the token - such as "send/receive", and a method such as "binary".

As soon as the client connects they may bind to assigned rooms.

## Tokens

A 'Token' is a unqiue ID or secret key used by a client to access the router through the ingress.
Its essentially a micro-user with its own permissions and connection settings. The
client assigns this token to the services and devices expecting to connect to the mesh.

The token should be unique to the task; such as one token per unique client. It may be prudent to use a single token for a range of similar clients.

Fundamentally the token should be _throw away_. Allowing a client to generate an unlimited amount and use them as temporary or persistent client keys. If in the event of a security exposure, the client should be allows to simply _regenerate_ a token, replacing existing - deleting old.


### Tokens for Share Spaces.

At times it may be prudent to use a token for many clients. For example many users connecting to a website chat bot. Each user may be using the token. In these cases we define a maximum connection count using that token, and internally we define a subnet-like naming convention for the token usage:

    socket:token/sub-count