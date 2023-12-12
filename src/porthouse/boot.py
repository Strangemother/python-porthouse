from pathlib import Path
import sys

from . import config
from .arguments import get_args
from . import log


def print_banner(args):
    log_level = args.log_level.upper()
    config_path = args.parsed_config if hasattr(args, 'parsed_config') else pargs.config

    has_conf = False
    if config_path is not None:
        has_conf = True
        config_path = str(Path(config_path).absolute().as_posix())

    lines = (f"\n\tPorthouse cli ... Fancy Banner ... \n"
             f"\t{log_level=}\n"
             )

    if has_conf is True:
        lines += f"\t{config_path=}\n"
    lines += f"\n"

    print(lines)


def main_run():
    log.d(f'__main__::main executor')
    return cli_run()


def cli_run():
    args = get_args()
    log.configure_from_args(args)
    config.configure_conf(args)

    if config.NO_BANNER is False:
    # if args.no_banner is False:
        print_banner(args)


    if hasattr(args, 'func'):
        return args.func(args)

    log.d('-- end -- ')
    # run.async_server(**vars(args))


if __name__ == '__main__':
    main_run()