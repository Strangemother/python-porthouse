from enum import Enum, auto
from ..denum import generate_enum
from ..dispatch.register import get_register


"""Import members from the dispatch register and convert to an Enum class

    class Methods(Enum):
        SUPERCAST = 'supercast'
        ROOMCAST =  'roomcast'
"""
members = {x.upper():x.lower() for x in get_register()}
Methods = generate_enum('Methods', members)


def keys():
    """Return a list of enum member instances, available within the `Methods` enum class.
    """
    return tuple(Methods)


def values():
    """Return the `.value` of each enum member from the `keys()` function.
    """
    ks = keys()
    return tuple(x.value for x in ks)

