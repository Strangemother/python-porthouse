# Inbound Message Processing and Routing

## Overview

In the WebSocket communication framework, inbound messages, whether in binary or text format, are intricately processed and routed to their intended destinations. These messages are associated with specific socket IDs, ensuring accurate delivery and traceability.

## Message Structure

Upon receipt, each message is characterized by the following attributes:

- **MessageID**: A unique identifier automatically generated for each message, ensuring distinctiveness and aiding in potential logging or debugging activities.

- **Client ID**: An identifier provided by the client, typically representing the user or device sending the message.

- **Socket ID**: An automatically generated identifier specific to the socket through which the message was received.

- **Message**: The core content or payload that the sender intends to communicate.

- **Additional Metadata**: Depending on the system's requirements, other metadata fields can be added to further describe the message.

This structure represents the raw form of the message as received directly from the socket.

## Message Routing Mechanism

The message routing system, henceforth referred to as the `router`, undertakes the following steps upon receiving a message:

1. **Message Wrapping**: The raw message is encapsulated within an `Envelope` class. While the envelope's metadata can be modified by the router, the root message typically remains unchanged.

2. **Target Identification**: The router reads the socket ID from the envelope to determine the target client, room, or broader audience. This could be a specific client, a room, or all currently connected entities.

3. **Message Broadcasting**: The router identifies all target sockets based on subscriptions and executes the `recv` method on each socket, ensuring the message is received by all intended recipients.

4. **External Routing**: In some scenarios, the receiving socket might represent another communication channel. In such cases, the message is routed out of the current router and into another system or router.

5. **Primary Pipe Mechanism**: Certain routers or rooms might be configured with a primary communication channel. If a message is received on this channel, it's forwarded to another designated server or system for further processing.

## Hops and Message Traceability

The `Envelope` class has the capability to register `hops`. Each hop represents a server and socket combination that the message has traversed.

- **Hop Count**: Represents the number of servers or systems the message has passed through. It provides an indication of the message's distance from its origin.

- **Hop Path**: A sequential list or trace of all servers and sockets the message has traversed. This aids in understanding the message's journey and can be crucial for debugging or performance analysis.

