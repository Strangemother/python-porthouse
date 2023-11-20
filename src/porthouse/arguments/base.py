import argparse
import sys


from . import installer, run
from .. import config as conf_module

__all__ = ['get_parsed_args', 'get_args', 'get_parser']


def get_parser():
    parser = argparse.ArgumentParser(prog='Porthouse',
                fromfile_prefix_chars='@',
                description='What the program does',
                epilog='Text at the bottom of help'
                )
    # parser.parse_args(['-f', 'foo', '@args.txt'])
    parser.add_argument('--log-level',
                action='store',
                default=conf_module.LOG_LEVEL,
                help='log level'
                )

    installer.apply_subparsers(parser)
    parser = apply_secret_options(parser, help=argparse.SUPPRESS)
    return parser


def get_pre_parser():
    parser = argparse.ArgumentParser(prog='Porthouse Secret Parser',
                fromfile_prefix_chars='@',
                add_help=False,
                # prefix_chars='+/',
                # exit_on_error=False,
                )
    return apply_secret_options(parser)


def apply_secret_options(parser, **kw):
    parser.add_argument('--soft-parse',
                action='store_true',
                default=False,
                **kw
                )
    parser.add_argument('--loud',
            action='store_true',
            default=False,
            # help="If True, don't error on known args"
            **kw
            )

    return parser


def get_args(argv=None):
    parser = get_parser()
    prep = get_pre_parser()

    prep_space, unknown = prep.parse_known_args(argv)

    print(prep_space)
    if prep_space.loud:
        prep.print_help()
        sys.exit(0)
    # parser._option_string_actions.update(prep._option_string_actions)

    f = parser.parse_args
    if prep_space.soft_parse is True:
        f = parser.parse_known_args

    # push the secrets into the args as suppressed
    #
    # help=argparse.SUPPRESS

    namespace = f(argv)
    if prep_space.soft_parse is True:
        namespace, namespace._unknown = namespace

    return namespace


def get_parsed_args(argv=None):
    v = get_args(argv)
    return vars(v)


if __name__ == '__main__':
    args = get_args()