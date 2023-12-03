from enum import Enum, auto

class Methods(Enum):
    SUPERCAST = 'supercast'
    ROOMCAST =  'roomcast'


def keys():
    return tuple(Methods)


def values():
    ks = keys()
    return tuple(x.value for x in ks)

