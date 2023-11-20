# ~Client Channel~ The Freeport.

> Designated the "Freeport" - Allowing a user to own a freeport of their information - The Freeport of Terry.

+ Every user has a freeport; it hosts all their account messages
+ They connect when required
+ It has no history, only _current_ events.
+ This is the users command-channel

Aside from the standard _rooms_ a client may generate, the client has their own _room_ by default. This is semi-transient, in which the room is always allocated to them, and all client items may connect to their room - but it doesn't exist as a waiting room. Thus history and other users are not applicable.

The client channel should be dedicated to annoucements and personal debug messages. Such as connection announcements across all rooms, or debug messages for errors.
This may be used for lost messages - under the client but did not reach a destination.

The client may always connect to their own channel to gain stats and manage their commands.

This can be naturally a broadcast room. And any device connected to this room will receive messaages.

A user does not need to create this room and any new sockets are seen within.

Clients can send messages to other clients, in a form of direct messaging. However the messages shouldn't send directly to the account name. Instead a secret account id is assigned to the user, and they can given these out as required. They may have many.