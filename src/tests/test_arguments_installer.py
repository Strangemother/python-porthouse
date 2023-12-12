from unittest import TestCase
from unittest.mock import patch
import runpy

from porthouse.arguments import installer
from porthouse.arguments.run import run_command_hook
from mocks import MethodSink


class TestArgumentsInstaller(TestCase):

    def test_install_subparser(self):
        item1 = {}
        item2 = {}
        installer.INSTALLERS = []
        installer.install_subparser(item1)
        installer.install_subparser(item2)
        assert len(installer.INSTALLERS) == 2
        self.assertSequenceEqual(installer.INSTALLERS, [item1, item2])


    def test_apply_subparsers_collects_subparser(self):
        subparser = MethodSink()
        subparser.add_parser.return_value = MethodSink()
        parser = MethodSink()
        parser.add_subparsers.return_value = subparser

        installer.apply_subparsers(parser)

        assert parser.add_subparsers.called == True

    def test_apply_subparsers_collects_subparser(self):
        parser = MethodSink(return_factory=MethodSink, deep_sink=True)
        installer.apply_subparsers(parser)
        assert parser.add_subparsers.call_count == 1

    def test_apply_subparsers_calls_installed_parsers(self):
        mock_subparsers_object = {}
        parser = MethodSink(return_value=mock_subparsers_object)

        # custom parser to install
        subparser = MethodSink()

        installer.INSTALLERS = [subparser]
        installer.apply_subparsers(parser)

        assert subparser.call_count == 1
        assert subparser.called_with(mock_subparsers_object)
        # ensure mock_subparser is called with the result from add_subparsers
