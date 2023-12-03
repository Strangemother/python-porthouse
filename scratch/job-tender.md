# Job Tender

We can setup a message response service to distribute messages for "tender". One or more nodes may respond to the tender with _capabilities_. The node originally presenting the message may select the _best node_ from the list of responses.

Fundamentally it allows focused message distribution through a range of possible nodes; and only the _preferred_ node receives the information.