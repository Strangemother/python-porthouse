
from .arguments import get_args

from loguru import logger
dlog = logger.debug

# from . import run

import sys


def print_banner(args):
    level = args.log_level.upper()

    lines = (f"\n\tPorthouse cli - ... Fancy Banner ... \n"
             f"\t{level=}\n"
             f"\n"
            )
    print(lines)


def main_run():
    dlog(f'__main__::main executor')
    return cli_run()


def cli_run():
    args = get_args()

    print_banner(args)

    level = args.log_level.upper()
    # global configure.
    logger.configure(handlers=[{"sink": sys.stdout, "level": level}])

    if hasattr(args, 'func'):
        return args.func(args)

    dlog('-- end -- ')
    # run.async_server(**vars(args))

## future
#
# jupyter run
# process/thread run