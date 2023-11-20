# Logging

`porthouse` applies two log levels for a running tool, the application `log-level` and a router `router-log-level`.

By default application level logging is set to `info` (less logging) and the router is set to `debug` (loguru default). For example:

    porthouse run -p 9005

Is akin to:

    porthouse --log-level=info run -p 9005 --router-log-level=debug

---

Here is an example of switching the log levels:

    porthouse --log-level debug run --router-log-level info -p 9005