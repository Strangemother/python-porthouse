import sys
import tomli


LOG_LEVEL = 'debug'

HOST = '127.0.0.1'
DEBUG = True
RELOAD = DEBUG
PORT = 0# 9004

BALANCE_PORTS = ()
BALANCE_ADDRESSES = (HOST, BALANCE_PORTS, )

INGRESS_APP = 'porthouse.ingress:app'

ROUTING = 'supercast'

mb1 = 1024 * 1024
mb16 = 16 * mb1

WS_MAX_SIZE = mb1

DEFAULT_PORTHOUSE_FILENAME = '.porthouse'



def configure_conf(namespace):
    """Given an argument namespace, mutate the attributes in this module to
    alter the internal configuration options of porthouse.

    This allowed the lib to `import config` without argument inspection.
    """
    # Apply options from porthouse [filename] to namespace.
    conf = namespace.parsed_config
    if conf is not None:
        merge_toml_to_config(conf)
    # apply any --param to config.PARAM if PARAM exists.
    merge_args_to_config(namespace)


def merge_toml_to_config(conf):
    res  = tomli.loads(conf.read_text())
    write_items(res)


def merge_args_to_config(namespace):
    keep = {}
    nks = vars(namespace)
    for key in globals().keys():
        if key.startswith('_'):
            continue
        val = nks.get(key.lower(), None)
        if val is not None:
            keep[key] = val

    write_items(keep)


def write_items(items):
    """Install the dictionary items into the module as the _config_ options
    of a porthouse instance.

        write_items({ 'key': 'value'})
    """
    target  = sys.modules[__name__]

    for k,v in items.items():
        print(' -- Writing', k, ' == ', v)
        setattr(target, k, v)
