"""
Note: event_loop_instance must be imported within the target test file,
to ensure the fixture is found automatically.

    from asyncsupported_testcase import (event_loop_instance,
                                        AsyncSupportedTestCase)

Import everything as a neat solution

    from asyncsupported_testcase import *

"""

import asyncio
import pytest
from unittest import TestCase


__all__ = ['event_loop_instance', 'AsyncSupportedTestCase']


@pytest.fixture(scope="class")
def event_loop_instance(request):
    """ Add the event_loop as an attribute to the unittest style test class. """
    request.cls.event_loop = asyncio.get_event_loop_policy().new_event_loop()
    yield
    request.cls.event_loop.close()


#@pytest.mark.asyncio(scope="class")
@pytest.mark.usefixtures("event_loop_instance")
class AsyncSupportedTestCase(TestCase):

    def get_async_result(self, coro):
        """ Run a coroutine synchronously. """
        return self.event_loop.run_until_complete(coro)
