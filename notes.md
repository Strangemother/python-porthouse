# Channels

A channel binds a range of clients to one backbone of communication. This allows the easy subdivision of tokens without polluting the event space of groups.

A single client may bind to many channels.
A transient channel may exist for the life of connected parties
parent channels may read sub channels automatically
The user has an automatic parent channel

All channels send events. These exist on `channel-name.events`


# Bridge

A bridge is similar to a bind, but the two ends of a bridge mount to another service - not strictly a client.

The bridge sends events and other primary later messages, effectively connecting the two services as if they're one. This is useful for sharing the connections of many clients through more than one ingress.

All clients on both sides of the bridge may communicate as if they're on the same ingress manager.
path of the manager is done through the leafd of the bridge.

