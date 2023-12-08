"""This register offers a mount point for future _dispatch_ methods, named in
the config and used upon message entry.
This function is used within the `router`, `methods` and consequently the `run`
for the arguments list.


By default the `roomcast` and `supercast` methods exist, append more with
`add_to_register`

    def dispatch_func(message):
        ...

    add_to_register('supercase', dispatch_func)

    register = get_register()
"""

from .supercast import supercast as supercast_dispatch_method
from .roomcast import roomcast as roomcast_dispatch_method


REGISTER = {
    'supercast': supercast_dispatch_method,
    'roomcast': roomcast_dispatch_method,
}

def get_register():
    return REGISTER


def add_to_register(name, func):
    REGISTER[name] = func