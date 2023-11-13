# Python Porthouse

> Streamlined Async Websocket Mesh Solution

`porthouse` is a Python library focused on asynchronous communication, primarily using Websockets. It's designed to simplify the creation of distributed architectures, enabling developers to concentrate on building functional logic rather than on complex meshing solutions.


Primary features:

+ Minimal (to zero) configuration setups
+ Plug and play broadcast and pub/sub features
+ Instant meshing and bridging
+ Easy to run and extend
+ Asynchronous and modular **to the bones**
+ no magic Websockets.


## Getting Started

Install the library:

    pip install porthouse

## Run your Porthouse

From the cli script:

    $> porthouse -h

as a module (FastAPI on uvicorn)

    $> py -m porthouse.run
    INFO:     Started server process [33512]
    INFO:     Waiting for application startup.
    2023-11-12 07:16:54.515 | DEBUG    | porthouse.primary:lifespan:47 - lifespan Startup
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://127.0.0.1:52181 (Press CTRL+C to quit)


In your code:

```py
from porthouse import run
run.async_server(debug=True)
```

Perhaps as a `uvicorn` app:

    python -m uvicorn porthouse.ingress:app --host 127.0.0.1 --port 0 --reload --log-level info
    INFO:     Started server process [33512]
    INFO:     Waiting for application startup.
    2023-11-12 07:16:54.515 | DEBUG    | porthouse.primary:lifespan:47 - lifespan Startup
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://127.0.0.1:52181 (Press CTRL+C to quit)


# What

Porthouse aims to be your silent partner when using WebSockets. This library offers a straightforward, almost invisible experience, perfectly suited for developers who value simplicity and efficiency.

With Porthouse, you can quickly set up local broadcast rooms for testing and prototyping, requiring zero initial configuration. It's designed to be a flexible backbone for your projects, compatible with a wide range of HTTP frontends and storage backends. Porthouse is all about empowering you to build and test solutions rapidly, without getting in your way.


# Why

Porthouse is a modern Python-based websocket library, evolved from the necessity to simplify real-time network communication. Leveraging the latest advancements in Python's asynchronous capabilities, it moves away from the complex multi-threaded architectures that were once required.

This library provides developers with a straightforward, efficient solution for managing websocket interactions. By focusing on simplicity and the strengths of Python's async features, Porthouse aims to streamline the development process, making it easier for developers to implement reliable, real-time network communication in their projects.