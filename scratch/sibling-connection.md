
A sibling connection can send commands on behave of the one channel
A client channel can send commands on behave of their system

Therefore commands and the coammdn channel may be reused.

A command can identify in and _out_ for each command. For example

    Disconnect
    SOCKET_ID

sent from the client channel would disconnect the id. Down to the client channel, this event announces a disconnect.

As a sibling and client channel cannot directly send messages, it's unlikely to be abused.

===

## Backpipe v RouterPipe


The backpipe is designed to exist within a peer mesh of relatives. They pump messages between each other in a more complex fashion using recipts and tendering

The router pipe is designed to ensure messages within a primary router are seen by another router in the form of a twin.
The routerpipe is more expected to be local, and may communicate with the primary router through functions - or a local pipe.

