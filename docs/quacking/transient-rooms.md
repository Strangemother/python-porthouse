# Transient Rooms

A _Room_ serves as a Porthouse modification of the standard _channels_ concept, where a user subscribes to a _room_, enabling broadcast messages across connected clients.

## Definition
A **Transient Room** defines a non-persistent room, where its existence is dynamic and ephemeral, rather than predefined and fetched from user subscriptions.

## Subscription Mechanism
A client socket may request to subscribe to a new transient room. If the requested room name does not exist, the socket will connect to the newly created room. Additional sockets are allowed to join the same transient room.

## Lifecycle Management
Once all participating sockets disconnect, the transient room ceases to exist, and the name becomes available for future use. The client is considered the _owner_ of the room for the duration of its activity.

# Peer Versus Peerless

The lifecycle of a Transient Room can be configured based on the socket interactions:

- **Peer Mode**: In peer mode, the room is designed to _close_ once the initiating socket disconnects. This action effectively ends all subscriptions to the room.
- **Peerless Mode**: Alternatively, a peerless room allows for the assignment of another connected socket as the _room owner_ upon the initiator's departure. This ensures room persistence until the last socket leaves.

Functionality within these modes can be adapted based on the specific requirements of the room's purpose and the rules governing socket interactions.
