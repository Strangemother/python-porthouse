import argparse
import sys

from .installer import install_subparser
from .. import config as conf
from .. import run as porthouse_run
from ..router import methods
from .. import log

"""
Arguments to accept:

    port = 0
    broadcast uris|ports
    ip address
    debug

    @file
"""

def automain():
    install_subparser(run_command_hook)


def run_command(namespace):
    log.i('Running porthouse async server')
    porthouse_run.async_server(**vars(namespace))


class Helps:
    routing_method = 'Assign how the messages are dispatched within the router. default: "%(default)s"'
    log_level = 'set the application logging level default: "%(default)s"'
    balance_ports = f'Balance Ports - default: "{conf.BALANCE_PORTS}"'
    host = 'Bind to an ip address or Ingress HOST - default: "%(const)s"'
    port = 'Ingress Port - default: "%(const)s"'
    app = 'Ingress Application - default: "%(const)s"'


def option(default=None, help=None, **params):
    """A helper function to assit with kwarg loadout for an argument
    """
    # add(*switches,**params)

    params['default'] = None
    if default is not None:
        params.setdefault('const', default)
        params.setdefault('nargs', '?')

    if help is not None:
        params['help'] = getattr(Helps, help, None)
    return params


def run_command_hook(subparsers):

    run_parser = subparsers.add_parser('run', aliases=('r',), help='Run')
    run_parser.set_defaults(func=run_command)
    add = run_parser.add_argument

    add('-a','--app', **option(
            type=str,
            default=conf.INGRESS_APP,
            help='app',
            dest='target',
            metavar='APP_STRING'
        ))

    add('-p','--port',**option(
            type=int,
            nargs='?',
            const=conf.PORT,
            default=None,
            help='port',
        ))

    add('-i','--host',**option(
            type=str,
            default=conf.HOST,
            help=Helps.host,
        ))

    add('-b','--balance-ports', **option(
            action='extend',
            nargs='+',
            ## Note bug: https://github.com/python/cpython/issues/110131
            ## means 'default' pollutes the extend list. This is annoying.
            # nargs='*',
            # action='store',
            type=int,
            default=conf.BALANCE_PORTS,
            help='balance_ports',
            const=None,
        ))

    add('-l','--router-log-level',
        action='store',
        default=conf.LOG_LEVEL,
        help=Helps.log_level
        )

    routing_choices = methods.values()
    add('-r', '--routing-method',
        action='store',
        default=routing_choices[0],
        help=Helps.routing_method,
        choices=routing_choices,
        # choices=['roomcast', 'supercast'],
        )

    add('--no-banner',
        action='store_true',
        default=conf.SUPRESS,
        # help=Helps.routing_method,
        )


    add('--garbage-collection',
        action='store',
        default='native',
        choices=['native', 'aggressive', 'peek', 'clock']
        # choices=['roomcast', 'supercast'],
        )


    return run_parser


automain()