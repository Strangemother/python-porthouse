import argparse
import sys


from . import installer, run
from .. import config as conf_module
from ..config import configure_conf

__all__ = ['get_parsed_args', 'get_args', 'get_parser']


import os

def get_parser():
    parser = argparse.ArgumentParser(prog='Porthouse',
                fromfile_prefix_chars='@',
                description='What the program does',
                epilog='Text at the bottom of help'
                )

    # Porthouse Config file, _optionally_ given before any  subapp.
    parser.add_argument('config', nargs='?', default=None)
    parser.add_argument('--config-file', default=None) # None for real default.

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

    namespace.parsed_config = resolve_config(namespace)
    return namespace

def get_parsed_args(argv=None):
    v = get_args(argv)
    configure_conf(v)
    return vars(v)


from pathlib import Path


def resolve_config(namespace):
    """The first optional positional argument accepts a config file or directory.
    If none are given the system will default to the _current_ directory
    (The `porthouse` startup directory).

    If the given path is a directory, resolve to a porthouse config file - also
    from the config.

    By default the porthouse configuration is `.porthouse` to promote non-commit.
    """
    conf = namespace.config
    filename = namespace.config_file
    default_filename = conf_module.DEFAULT_PORTHOUSE_FILENAME
    current_dir = os.getcwd()
    """If the config is a directory, resolve filename.
    If conf is file,
        if also filename arg - raise error.
    """

    if conf is None:
        return None

    # Is file or DIR
    cp = Path(conf)
    filepath = cp
    if cp.is_dir():

        if cp.exists() is False:
            # Raise bad dir
            s = f'Directory does not exist {str(cp)=}'
            raise Exception(s)

        # dir, resolve file `filename`
        filepath = cp / (filename or default_filename)

    nf = filepath is None
    exists = filepath.exists()
    if nf or (exists is False):
        # raise bad file.
        fullpath = str(filepath.absolute())
        s = f'File does not exist {fullpath=}'
        raise Exception(s)

    print('Good path', filepath)
    return filepath
    # else:
        # for None conf, assume _current directory_
        # with no errors




if __name__ == '__main__':
    args = get_args()