## Note (After Below)

+ Should implement django async views for socket integration.
+ A Service needs a backpipe
    + To pump messages from service to the mesh
        + Live Change adaption
+ Integrate puddles to the router
+ build an 'adapter' for other platforms: fastapi, sanic, flask, websockets
    Question is - is this required. As the porthouse router abstracts the
    process enough, to allow a user to choose their own frontend and pump messages.
    Potentially adding one strong frontend to a router (e.g. fastapi) and provide
    a base adapter for devs to inherit.


### Live Change Adaption

The service will administer rooms and tokens. When an owner performs these changes, they should progagate immediately across the mesh. For example if an owner assigns a new room to a client, the client should immediately recieve the update

    1. Owner/User deploys a tokenized client
    2. Owner changes token subscription (Add 1 room "foo")
    3. Client receives room "foo" message

Same with revokations of a token:

    1. Clients are connected via token ("123") only.
    2. Owner deletes token "123"
    3. All token clients revoke token.
    4. Clients have no authentication token; and drops.

## Next (Nov 2023)

### User Account:

+ Accounts
+ Rooms
+ Tokens

A user should be able to:

+ Create an account
+ Login
+ Administer rooms
+ Work with tokens.

A user should be able to create their rooms, and access them from a HTML interface




---

### Python Client

The client should provide a number of key features to a system

#### Message pump

Given a configured node, a `porthouse.pump [message]` should connect, and dispatch a message.


#### Local Envelope

A user may wish to send large or complex data through the pipe. This can be managed by the user, alternatively the can use the local tools to wrap and dispatch messages without the overhead of writing a solution.

```py
from porthouse import Envelope

large_data = bytes(...) # 10 meg

en = Envelope(message=large_data)
for chunk in en.chunks(1024): #1024 kb chunks.
    socket.send(chunk)

## Also
connection = porthouse.connect("@conf")
connection.send(en)
connection.close()
```

