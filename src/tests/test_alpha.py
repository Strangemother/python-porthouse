import asyncio
import pytest

from porthouse import run


import os
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec
from importlib import reload
from unittest import TestCase
from unittest.mock import MagicMock, patch

from pathlib import Path
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


@pytest.mark.asyncio
async def test_an_async_function():
    # task =  run.main(await_task=False)
    # print('Run task.', task)
    # await task
    # print('Ran task.', task)

    # await asyncio.sleep(3)
    # result = await call_to_my_async_function()
    assert 1 == 1
