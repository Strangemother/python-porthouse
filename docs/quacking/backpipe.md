# BackPipe Component in Porthouse Library

The BackPipe module is a core component of the Porthouse library, designed for peer-to-peer messaging within a network of routers.

It serves as a direct communication conduit between routers, bypassing the frontend, to facilitate centralized and mesh network communications.


## Features

- Operates as an independent socket, allowing asynchronous communication within the mesh network.
- Functions as a client to the router, handling internal messages.
- Capable of being a part of a mesh network where it can either handle messages in a balanced or unbalanced network load.
- Can be used in scenarios where a router is designated as a hop point, solely managing multiple BackPipes for message ferrying.


## Purpose

- Designed to offset critical messages from the frontend, allowing the frontend to either remain closed or stay outside of internal routing.
- Essential for internal network communications, particularly in complex or heavily loaded network environments.


## Implementation

- As a self-contained WebSocket, it maintains independence from the frontend, ensuring asynchronous communication with the backend.

## Example Usage


```python
from backpipe import BackPipe

# Initialize the BackPipe
backpipe = BackPipe(response_handler=my_response_handler)

# Connect the BackPipe to a router
router_uri = "ws://localhost:8000/token"
backpipe.connect(router_uri)

# Example response handler function
async def my_response_handler(message):
    print(f"Received message: {message}")

# Send a message through the BackPipe
await backpipe.send("Hello, Router!")

# Close the BackPipe connection when done
await backpipe.close()
