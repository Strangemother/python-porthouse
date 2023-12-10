from unittest import TestCase
from unittest.mock import patch
import runpy


class TestMain(TestCase):

    @patch('porthouse.boot.main_run')
    def test___main__(self, main_run_patch):
        """Assert `py -m porthouse` executed the main() function
        """
        res = runpy.run_module('porthouse', run_name='__main__')
        main_run_patch.assert_called()

    @patch('porthouse.boot.main_run')
    def test___main___import(self, main_run_patch):
        """Assert `import porthouse.__main__` does not executed the main() function
        """
        res = runpy.run_module('porthouse', run_name='porthouse.__main__')
        main_run_patch.assert_not_called()
