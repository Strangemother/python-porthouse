from .arguments import get_args
# from loguru import logger
from . import log
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
    log.d(f'__main__::main executor')
    return cli_run()


def cli_run():
    args = get_args()

    print_banner(args)

    level = args.router_log_level.upper()
    # global configure.
    log.logger.configure(handlers=[{"sink": sys.stdout, "level": level}])

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