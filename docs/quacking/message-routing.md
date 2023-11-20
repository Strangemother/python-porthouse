

A message in from the client has a destination. In most cases this is a _room_ containing many connected sockets.

When the message is sent into the router, the message is first sent to the local rooms.

If the local room does not exist (the message is undelivered) it should be dispatched to through the backpipe to the next router.

Rather than the dispatching the real message, a "tender" is sent across the wire. This is a signal from router A to the _next_ routers; "there is a message for X".

In this case the tender is a delivery. A router should read this message and determine if _it_ is the target destination, Upon which the router responds with a request for the full message.

If the tender is not met by the _current_ router, it's passed onto the next until a tender is resolved.

    Router A (tender)  -> Router B [pass] -> Router C [ignore]
                                          -> Router D [Accept]
    Router A (receive) <- Router B [pass] <- (address "D")

At this point the router A should connect to router D directly, through the tender address.