import argparse
import sys

from .installer import install_subparser
from .. import config as conf
from .. import run as porthouse_run
from ..router import methods

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
    print('run command')
    porthouse_run.async_server(**vars(namespace))



class Helps:
    routing_method = 'Assign how the messages are dispatched within the router. default: "%(default)s"'
    log_level = 'set the application logging level default: "%(default)s"'
    balance_ports = f'Balance Ports - default: "{conf.BALANCE_PORTS}"'
    host = 'Bind to an ip address or Ingress HOST - default: "%(default)s"'
    port = 'Ingress Port - default: "%(default)s"'
    app = 'Ingress Application - default: "%(default)s"'


def run_command_hook(subparsers):

    run_parser = subparsers.add_parser('run', aliases=('r',), help='Run')
    run_parser.set_defaults(func=run_command)
    add = run_parser.add_argument

    add('-a','--app',
            type=str,
            default=conf.INGRESS_APP,
            help=Helps.app,
            dest='target',
            metavar='APP_STRING'
        )

    add('-p','--port',
            type=int,
            default=conf.PORT,
            help=Helps.port,
        )

    add('-i','--host',
            type=str,
            default=conf.HOST,
            help=Helps.host,
        )

    add('-b','--balance-ports',
            action='extend',
            nargs='+',
            ## Note bug: https://github.com/python/cpython/issues/110131
            ## means 'default' pollutes the extend list. This is annoying.
            # nargs='*',
            # action='store',
            type=int,
            default=None,
            help=Helps.balance_ports,
        )

    add('--router-log-level',
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


    add('--garbage-collection',
        action='store',
        default='native',
        choices=['native', 'aggressive', 'peek', 'clock']
        # choices=['roomcast', 'supercast'],
        )


    return run_parser


automain()