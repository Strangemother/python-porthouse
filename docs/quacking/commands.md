# Command and Message Formatting for WebSocket Communication

## Introduction

WebSocket connections facilitate real-time bidirectional communication between the client and the server. To perform specific actions, clients must send well-defined commands to the server. This document describes the command formats supported by our WebSocket server.

## Supported Communication Methods

Commands can be sent using one of the following methods, depending on the use case and client capabilities:

- **Binary**: Commands are sent as byte streams.
- **Text**: Commands are sent as plain text strings.
- **JSON**: Commands are sent as JSON objects.

Commands should be formatted according to the chosen method and must be correctly parsed by the server upon receipt.

## Command Formats

### Text Commands

Text commands offer a simple and human-readable option for interaction. They should follow a predefined syntax similar to CLI commands. Parsing on the server is handled via a switch-case-like structure in Python, typically implemented with if-elif-else statements or dictionary mappings.

#### Example Usage

Client sends a command to subscribe to rooms "alpha" and "beta":

    SUBSCRIBE alpha beta

Server acknowledges the subscription:

    < Subscribed to rooms: alpha, beta

### JSON Commands

When using JSON, commands are structured objects that provide clarity and ease of expansion for complex instructions. JSON is especially useful when dealing with a variety of potential command options and settings.

#### Example Usage

Client sends a JSON object to subscribe to multiple rooms:

```json
> {"action": "subscribe", "rooms": ["alpha", "beta"]}
```

Server responds with a JSON object confirming the subscription:


    < {"response": "subscribed", "rooms": ["alpha", "beta"]}

### Binary Commands

Binary commands are intended for scenarios where efficiency is paramount. Upon receiving a binary message, the server will decode it to a text command, assuming a standard encoding such as ASCII or UTF-8.

#### Handling Binary Data

The server converts binary messages into a text-equivalent format before parsing them as commands. This ensures consistency across different communication methods and allows for the use of the same command-parsing logic.

### Conclusion

Each command format has its own use cases and benefits. Clients should choose the most appropriate method based on their needs, while ensuring that commands are correctly structured for the server to parse and execute. It's crucial for developers to implement robust parsing and validation mechanisms on the server to handle these commands securely and efficiently.

