## Porthouse

> A platform to host websocket information and connection without limit

Version 1 exposed the necessity of socket abstraction, and state management.
In the previous instance single socket was assigned an id; and the state of the socket lived within the process.

Coupled with a ugly _room_ design, this caused limitation to the authentication flow.

+ Everything should be async to the core
+ Multiprocessing by nature (puddles)
+ Independent state machine to manage socket entries (sequences)


Taken from projects/websocket/docs/architecture_notes.md

Replicating the old bridge system:

+ Ingress server acts can act as broker
    + Sending messages to other servers through a custom bridge



### Endpoints

An owner can create a public endpoint for a room. Users can access the room
An endpoint may be the primary bridge (the root address), a clients custom address, or the room address.

    ws://primary.com
        to lobby
        auth
        gain client  access
        access room
        messages

    ws://client.primary.com
        auth
        gain client access
        access room
        messages

    ws://domain.com/room
        access room
        messages


The room is unique, as it may be public or private. Therefore _access room_ encompasses room rules, one of which may be _client auth required_.

Access Routines:

+ A single hit through the endpoint
    + A form _POST_
+ A single-shot message
    + open, message, close
+ client
    + open, message ... message, close


## Room

A _Room_ is a single environment for many clients
    + Many clients cross communicating
    + Incoming rules

A room may _broadcast_ to every client, unless the sender specifies a receiver list
    unless rules override this

### Rules

Room Rules define a list of access and send permissions for incoming clients. These rules govern how users can initial connect, and how messages format through transmission.

Generic rooms may allow a selected client list (and their sockets) to send in JSON format. Public rooms allow many anonymous clients with limits.
Entry rules may consist of passwords, 2-factor or other auth.


### Room Types

A Room holds many sockets, each as a receiver of messages from other sockets in the room.
A room is both transient and persistent. A 'spaces' module will provide a list of available rooms. Owner clients can generate rooms on-the-fly.

#### Transient Room

A Transient Room is a room without persistent data, generated by a client for live connection. A client flagged as 'primary' can generate rooms through a command `NEW ROOM [name]`. This may also define rules

New clients may connect to the room through it's unique name and message clients accordingly. When all clients leave the room naturally disappears.
This is useful for mesh coms, where two+ clients would like to communicate in a unique room - but generating a persistent room for these requirements would be costly.

#### Persistent Room

A Persistent Room is created before clients enter and defines rules stored in the database. This includes full time personal client rooms created by an owner.


## Client

A Client is a user or owner, connected through an endpoint, connected to the mesh.


## Messages

Messages through the sockets are as raw as possible.

+ Both binary (bytes) and text
+ Without alteration
+ Unless Rules apply

The room governs the allowed message types and can designate a the message format. The input message may be text or bytes, the room accepts this and converts it to the preferred (if required).
For example An FTP room accepts text strings, and performs FTP commands.
Files through the same pipe are converted to a PUT etc.

JSON rooms are most likely for frontend bound client and rooms. The sockets sends json formatted text for it to be send in a good format.
Meta data may bind to the object - but this is very optional
The receiver accepts a message in the format specific to the client type, such as an _object_ in javascript or a _dict_ in python.


## Sockets

A socket is a single connection to the mesh, usually owned by a _client_. In general one client has one socket but it's possible for more, for example a multi-socket client in js.
To define, a client is a _user_ or machine, using a single pipe to the mesh. The socket is the information binding the client to the mesh. If the client performs `connect()` using two unique addresses, or the same endpoint twice this generates two unique _sockets_, bound to the same client.

The client handles the messages as per unique sockets.
A single socket may subscribe to multiple rooms
Upon entry a socket usually starts in the lobby,
after auth is complete they're send to a room, or their own space (connected with no subscriptions)

