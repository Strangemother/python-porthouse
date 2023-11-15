import argparse
import sys

"""
Arguments to accept:

    port = 0
    broadcast uris|ports
    ip address
    debug

    @file
"""


def get_parser():
    parser = argparse.ArgumentParser(prog='Porthouse',
                fromfile_prefix_chars='@',
                description='What the program does',
                epilog='Text at the bottom of help')
    # parser.parse_args(['-f', 'foo', '@args.txt'])

    parser.add_argument('--foo', action='store_true', help='foo help')

    subparsers = parser.add_subparsers(help='sub-command help')

    run_parser = subparsers.add_parser('run', help='Run')
    run_parser.add_argument('bar', type=int, help='bar help')

    # create the parser for the "b" command
    parser_b = subparsers.add_parser('b', help='b help')
    parser_b.add_argument('--baz', choices='XYZ', help='baz help')

    return parser


def get_args(argv=None):
    parser = get_parser()
    namespace, unknown = parser.parse_known_args(argv)
    namespace._unknown = unknown
    return namespace

