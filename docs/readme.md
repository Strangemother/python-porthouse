# Python Porthouse 🏢

[![Upload Python Package](https://github.com/Strangemother/python-porthouse/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Strangemother/python-porthouse/actions/workflows/python-publish.yml)
![PyPI](https://img.shields.io/pypi/v/python-porthouse?label=python-porthouse)
![PyPI - Downloads](https://img.shields.io/pypi/dm/python-porthouse)


> Streamlined Async Websocket Mesh Solution

`porthouse` is a Python library focused on asynchronous communication, primarily using Websockets. It's designed to simplify the creation of distributed architectures, enabling developers to concentrate on building functional logic rather than on complex meshing solutions.

1. Have Python
2. `pip install porthouse`
3. Run it.

```bash
$> porthouse run
INFO:     Uvicorn running on http://127.0.0.1:52181 (Press CTRL+C to quit)
```

🚀 Broadcasting on all cylinders!


## 🌟 Key Features

+ Zero-Configuration: Set up in moments, not hours.
+ Broadcast & Pub/Sub: Effortless data dissemination.
+ Instant Meshing: Create flexible, interconnected networks swiftly.
+ User-Friendly: Simple to operate, simple to scale.
+ Asynchronous Core: Experience the full power of Python's async capabilities.
+ Transparent Websockets: No hidden complexities, just pure functionality.


## 💡 Why Porthouse?

Porthouse is developed as a pragmatic solution for developers dealing with the complexities of real-time WebSocket communication. Originating from a necessity to simplify intricate network interactions, it serves as a transparent tool intended to promote WebSockets as a single-asset solution, designed to be a 'no opinion' platform.

> Our primary aim with Porthouse is to demystify and streamline real-time socket communication. Our focus is on making WebSockets more accessible and manageable.


## Installation

Install the library:

```bash
pip install porthouse
```

## 🚀 Getting Started

Command Line Interface:

```py
$> porthouse run -h
```

As a module (FastAPI on uvicorn)

```bash
$> py -m porthouse.run
...
INFO:     Uvicorn running on http://127.0.0.1:52181 (Press CTRL+C to quit)
```

Directly in your code:

```py
from porthouse import run
run.async_server(debug=True)
```

As a `uvicorn` app:

```bash
python -m uvicorn porthouse.ingress:app --host 127.0.0.1 --port 0 --reload --log-level info
...
INFO:     Uvicorn running on http://127.0.0.1:52181 (Press CTRL+C to quit)
```



## 💡 Why Porthouse?

Porthouse is developed as a pragmatic solution for developers dealing with the complexities of real-time WebSocket communication. Originating from a necessity to simplify intricate network interactions, it serves as a transparent tool intended to promote WebSockets as a single-asset solution, designed to be a 'no opinion' platform.

> Our primary aim with Porthouse is to demystify and streamline real-time socket communication. Our focus is on making WebSockets more accessible and manageable.


# What

Porthouse aims to be your silent partner when using WebSockets. This library offers a straightforward, almost invisible experience, perfectly suited for developers who value simplicity and efficiency.

With Porthouse, you can quickly set up local broadcast rooms for testing and prototyping, requiring zero initial configuration. It's designed to be a flexible backbone for your projects, compatible with a wide range of HTTP frontends and storage backends. Porthouse is all about empowering you to build and test solutions rapidly, without getting in your way.


# Why

Porthouse is a modern Python-based websocket library, evolved from the necessity to simplify real-time network communication. Leveraging the latest advancements in Python's asynchronous capabilities, it moves away from the complex multi-threaded architectures that were once required.

This library provides developers with a straightforward, efficient solution for managing websocket interactions. By focusing on simplicity and the strengths of Python's async features, Porthouse aims to streamline the development process, making it easier for developers to implement reliable, real-time network communication in their projects.