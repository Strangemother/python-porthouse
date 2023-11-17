
INSTALLERS = []

def apply_subparsers(parser):

    subparsers = parser.add_subparsers(help='sub-command help')

    for subparser_installer in INSTALLERS:
        subparser_installer(subparsers)


def install_subparser(func):
    INSTALLERS.append(func)