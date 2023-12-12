"""# Config.

The `config` module acts as a centralised location for concurrent settings,
applied through the library, terminal, and config files.

Within the app call upon  a config option as normal:

    from porthouse import config
    config.HOST

When the application is created, the pre merging of terminal options will
alter these parameters before the sub application executes.

Only constants from this config file will be installed from the terminal.

    porthouse run --host 0.0.0.0 --something else
    conf.HOST == '0.0.0.0'

The local .porthouse file is TOML, applied into this config module using
`merge_toml_to_config(conf:Path)`
"""
import sys
import tomli
from . import log

SUPRESS = '==supress=='
LOG_LEVEL = 'debug'

HOST = '127.0.0.1'
DEBUG = True
RELOAD = DEBUG
PORT = 0# 9004
NO_BANNER = False
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
    return merge_args_to_config(namespace)

def merge_toml_to_config(conf):
    print(f'Loading: {conf}')
    res  = tomli.loads(conf.read_text())
    write_items(res)


def merge_args_to_config(namespace):
    keep = {}
    nks = vars(namespace)
    for key in globals().keys():
        if key.startswith('_'):
            continue
        val = nks.get(key.lower(), None)
        if val in (None, SUPRESS):
            continue
        keep[key] = val
    write_items(keep)
    return keep


def write_items(items):
    """Install the dictionary items into the module as the _config_ options
    of a porthouse instance.

        write_items({ 'key': 'value'})
    """
    target  = sys.modules[__name__]

    for k,v in items.items():
        log.t(f'Writing {k} = {v}')
        setattr(target, k, v)
