# Envelopes

An Envelope is the first routine the router performs when accepting a message. The message isn't usually affected by the router. Instead the router applies meta data to the editable envelope. This includes:

    Message ID
    Message
    DateTime
    Hope
    Server
    ...

servers and rooms can read the envelope. Users usually receive the message within, and potentially an envelope result in the debug channel.
