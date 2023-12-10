from unittest import TestCase
from unittest.mock import patch

from argparse import ArgumentParser
import argparse

from porthouse.arguments.base import get_parser, get_pre_parser


class TestArgumentBase(TestCase):


    @patch('argparse.ArgumentParser')
    @patch('porthouse.arguments.installer.apply_subparsers')
    @patch('porthouse.arguments.base.apply_secret_options')
    def test_get_secret_options_call(self, mock_apply_secret_options, mock_apply_subparsers, MockArgumentParser):
        """Assert the parser is given to apply_secret_options during setup."""
        result = get_parser()
        res = MockArgumentParser.return_value
        mock_apply_secret_options.assert_called_with(res, help=argparse.SUPPRESS)

        result = get_pre_parser()
        res = MockArgumentParser.return_value
        # without supression
        mock_apply_secret_options.assert_called_with(res)


    @patch('porthouse.arguments.installer.apply_subparsers')
    def test_get_parser(self, mock_apply_subparsers):
        _parser = get_parser()
        assert isinstance(_parser, ArgumentParser)
        mock_apply_subparsers.assert_called_with(_parser)
        # mock_apply_secret_options.assert_called_with(_parser)


    @patch('porthouse.arguments.installer.apply_subparsers')
    def test_get_pre_parser(self, mock_apply_subparsers):
        _parser = get_pre_parser()
        assert isinstance(_parser, ArgumentParser)
        mock_apply_subparsers.assert_not_called()