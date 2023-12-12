# Porthouse: A Comprehensive WebSocket Platform

Porthouse is a robust platform designed to host websocket information and connections without limitations. This document provides an overview of its architecture, functionalities, and design principles.

## Introduction

Porthouse aims to address the challenges faced in its first version, which highlighted the need for socket abstraction and state management. The initial design had a single socket assigned an ID with its state residing within the process. This, combined with a suboptimal room design, posed challenges to the authentication flow.

## Core Principles

- **Asynchronous Operations**: Every operation within Porthouse is asynchronous.
- **Multiprocessing**: The platform inherently supports multiprocessing, referred to as "puddles."
- **State Management**: An independent state machine manages socket entries, known as "sequences."

## System Components

### 1. Bridge System

The old bridge system is replicated in Porthouse, where:
- The ingress server can function as a broker, facilitating message transmission between servers through a custom bridge.

### 2. Authentication

For authentication:
- A user must possess a User object.
- Users are required to have an account and maintain their session ID.

### 3. Endpoints

Endpoints are the gateways for users to interact with rooms. They can be:
- The primary bridge (root address).
- A client's custom address.
- The room's address.

The room's accessibility can be public or private, with potential requirements for client authentication.

### 4. Room

A room is an environment where multiple clients can interact. Features include:
- Cross-communication between clients.
- Broadcasting capabilities to all clients, with potential exceptions based on sender specifications or room rules.

#### Room Rules

These define access and message transmission permissions for clients. They can dictate:
- Connection initiation.
- Message format during transmission.
- Entry requirements, such as passwords or two-factor authentication.

#### Room Types

Rooms can be either transient or persistent:

- **Transient Room**: Temporary rooms without persistent data. They are client-generated for live connections and disappear once all clients leave.

- **Persistent Room**: Pre-established rooms with rules stored in a database. They persist even without active clients.

### 5. Client

A client can be a user or owner connected to the mesh via an endpoint.

### 6. Messages

Messages transmitted through sockets are kept as raw as possible, either in binary (bytes) or text format. The room determines the allowed message types and can specify the message format.

### 7. Sockets

A socket represents a single connection to the mesh, typically owned by a client. While a client usually has one socket, multiple sockets are possible. Sockets facilitate the connection between the client and the mesh, and a single socket can subscribe to multiple rooms.
