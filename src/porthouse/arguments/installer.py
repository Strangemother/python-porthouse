
INSTALLERS = []

def apply_subparsers(parser):
    """Collect the `subparsers` from the `parser.add_subparsers`,
    and iter all INSTALLERS, calling each function within the list, providing
    the subparsers object.

    return None
    """
    subparsers = parser.add_subparsers(help='sub-command help')

    for subparser_installer in INSTALLERS:
        subparser_installer(subparsers)


def install_subparser(func):
    INSTALLERS.append(func)