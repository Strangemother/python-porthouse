from .arguments import get_args
# from loguru import logger
from . import log
# from . import run

import sys

from pathlib import Path

def print_banner(args):
    level = args.log_level.upper()
    conf = args.parsed_config if hasattr(args, 'parsed_config') else pargs.config

    if conf is not None:
        conf = str(Path(conf).absolute().as_posix())

    lines = (f"\n\tPorthouse cli - ... Fancy Banner ... \n"
             f"\t{level=}\n"
             f"\t{conf=}\n"
             f"\n"
            )
    print(lines)


def main_run():
    log.d(f'__main__::main executor')
    return cli_run()

from .config import configure_conf

def cli_run():
    args = get_args()
    log.configure_from_args(args)

    print_banner(args)

    configure_conf(args)

    if hasattr(args, 'func'):
        return args.func(args)

    log.d('-- end -- ')
    # run.async_server(**vars(args))


if __name__ == '__main__':
    main_run()
## future
#
# jupyter run
# process/thread run