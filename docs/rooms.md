# Room: A WebSocket Channel Abstraction

## Overview

In the context of WebSocket communication, a `Room` serves as an abstraction over the traditional concept of a "channel". It provides a unified space where users can subscribe and receive broadcasted messages from all participants within that space. The analogy of a 'room' or 'house' is employed to offer a more intuitive understanding of this communication paradigm.

## Architecture

### Subscribers and Protocols

A `Room` aggregates multiple subscribers under a unified set of protocols and rules. It acts as a mediator, ensuring that messages are transmitted across clients and subscribers in adherence to the defined protocols. This centralized management ensures consistency and order within the communication environment.

### Message Governance

The `Room` is responsible for governing the flow and format of messages. It ensures that messages are broadcasted to all subscribers, manages message queues, and handles potential issues like message collisions or buffer overflows.

## Ruleset

The behavior and interaction within a `Room` are governed by a predefined set of 'rules'. These rules determine:

- **Access Control**: Who can join or leave the room.

- **Message Allowances**: This includes constraints like:
  - Message count limits: Maximum number of messages a user can send in a given time frame.
  - Message size limits: Maximum size of individual messages.
  - Message rate: Frequency at which messages can be sent.
  - User limits: Maximum number of users allowed in a room.

- **Interaction Protocols**: How messages are formatted, validated, and transmitted.

### Room Accessibility: Public vs. Private

- **Public Room**: Such rooms are openly listed and accessible to all users. They are designed for broader communication where the entry barrier is minimal.

- **Private Room**: These rooms are not publicly listed and require specific access rights or credentials to join. They are suitable for more confidential or targeted communications.
