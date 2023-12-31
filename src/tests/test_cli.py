from unittest import TestCase

class TestCLIRun(TestCase):

    def test_cli_run(self):
        """Assert the cli module has a run method.
        """
        from porthouse import cli
        assert hasattr(cli, 'run')