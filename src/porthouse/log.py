import sys
from loguru import logger

dlog = logger.debug
elog = logger.error
t = logger.trace
i = logger.info
d = dlog
e = elog

__all__ = ['elog', 'dlog']


def configure_from_args(args):

    level = args.log_level
    if hasattr(args, 'router_log_level'):
        level = args.router_log_level

    level = resolve_level(level).upper()

    dlog(f'Setting level {level}')
    logger.configure(handlers=[{"sink": sys.stdout, "level": level}])


LEVELS = (
    'trace',
    'warning',
    'debug',
    'error',
    'info',
)


def resolve_level(value, default=None):
    """Given a partial word of a log level, return the full word
    """
    lv = value.lower()
    for level in LEVELS:
        if level.startswith(lv):
            return level#.upper()
    return default