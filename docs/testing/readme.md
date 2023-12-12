# Testing

The async functionality can be slightly tricky due to the nature of executing `async` methods within a sync environment. To assist with this some features are supplied to help run tests.

## Run

To run the tests we can use standard `pytest`

```bash
$> pytest -vs
```

## Async Tests

The `AsyncSupportedTestCase` provides some tools designed support async tests. This class inherits the standard `TestCase`:

```py
from asyncsupported_testcase import *

class TestDispatchRoomcast(AsyncSupportedTestCase):

    def test_roomcast(self):
        assert 1 == 1
        self.assertTrue(True)
```

The support library is designed to be `__all__` imported (`*`) as the event loop must execute within the same context as the TestCase.

The `asyncsupported_testcase.*` imports:

+ AsyncSupportedTestCase: The `TestCase` extended class.
+ event_loop_instance: the function to execute the event loop.

### Executing Async Code

The tests do not run in an asyncronous event loop, we must _submit_ the work and read the results. The function `AsyncSupportedTestCase.get_async_result(cororoutine)` will fetch and return the result from the async `Future`.


```py
from asyncsupported_testcase import *


async def my_async_func(name, age):
    ...
    return age * 10


class TestExample(AsyncSupportedTestCase):

    def test_mytest(self):

        coro = async_func("Bob", 5)
        result = self.get_async_result(coro)

        assert result == 50
```

We can use `self.get_async_result` for any async functionality.


### Async Patching

We can patch async methods with `mocks.AsyncMethodCallStats`

```py
from mocks import *
from asyncsupported_testcase import *

class TestDispatchRoomcast(AsyncSupportedTestCase):
    # test that the roomcast function
    #
    def test_roomcast(self):
        send_to_result = {'some': 'result'}

        router = MockRouter()
        router.send_to = AsyncMethodCallStats(return_value=send_to_result)

        coro = my_async_func(router)
        result = self.get_async_result(coro)

        # sends to the _given_ sockets
        assert router.send_to.called_with(sockets_ids, websocket, msg)
        # The result should be the routed value.
        assert result == send_to_result
```

It acts similar to a patch, were we can _ask_ how it was used:

```py
assert router.send_to.called_with(sockets_ids, websocket, msg)
```

+ `call_count`
+ `called`
+ `calls`
+ `called_with(*a, **kw)`
+ `return_value`

An `AsyncMethodCallStats` may replace any existing async function, and will execute in the event loop as expected.


### Method Sink

A simplified mocking utility, allowing the replacement of methods to capture call stats. Used in place of a regular Mock or MagicMock, allowing usage within an async environment.

```py
from mocks import MethodSink, MockWebSocket
from porthouse.router import Router

router = Router()
router.access_rules = MethodSink()
router.access_rules.is_valid.return_value = 101

client = MockWebSocket()
rule_is_valid = adapter.validate_accept(client)

assert rule_is_valid == 101
assert router.access_rules.is_valid.call_count == 1
```

A `return_factory` is a functional call for a `return_value`. This can return a MethodSink()

```py
from mocks import MethodSink

parser = MethodSink(return_factory=MethodSink)
parser.subparser.submethod('cake')

assert parser.subparser.submethod.call_count == 1
```

This can be nested, allowing a `deep_sink` of methods.

Here we have a parser, that returns a subparser when called. The subparser has a method `add_parser`, that returns a complex object. In each case we can _sink_ until all are manually mocked:

```py
from mocks import MethodSink

subparser = MethodSink()
subparser.add_parser.return_value = MethodSink()
parser = MethodSink()

parser.add_subparsers.return_value = subparser
```

With `deep_sink=True` all subcalls of a `MethodSink` return a MethodSink:

```py
from mocks import MethodSink

# same as above
parser = MethodSink(return_factory=MethodSink, deep_sink=True)
```

Notice the `return_factory` instead of a `return_value`, as this ensures a fresh `MethodSink` is _called_ rather than returning the same instance.


### Mock Objects

Some mock objects exist for free use, they're prepared with functions similar to the methods found on the standard mirrored object.

+ MockRouter
+ MockClient
+ MockClientState
+ MockWebSocket
+ MockTokens


#### MockRouter

Apply in place of a router:

```py
...

router = MockRouter()
router.filter_allowed_destinations = AsyncMethodCallStats(return_value=allowed)
router.gather_sockets = AsyncMethodCallStats(return_value=sockets_ids)
router.send_to = AsyncMethodCallStats(return_value=send_to_result)

websocket = MockWebSocket()
websocket.socket_id = origin_socket_id


from porthouse.envelope import Envelope
from porthouse.dispatch.roomcast import roomcast

msg = Envelope({'text': 'banana'}, 'owner')


coro = roomcast(router, websocket, msg)
result = self.get_async_result(coro)

...
```


# Examples

Test a dispatch method such as `roomcast`

```py
from unittest.mock import patch
from mocks import *
from asyncsupported_testcase import *

from porthouse.envelope import Envelope


class TestDispatchRoomcast(AsyncSupportedTestCase):
    # test that the roomcast function

    def test_roomcast(self):
        """Test the `porthouse.dispatch.roomcast.roomcast` function
        + It sends to the allows sockets
        + The result is the send_to result.
        """

        # Some example args.
        allowed = (1,2,4)
        origin_socket_id = '320f9j029jf 02'
        sockets_ids = ('A', 'B', 'C', origin_socket_id)
        send_to_result = {'some': 'result'}

        # Setup a router with some patches.
        router = MockRouter()
        router.filter_allowed_destinations = AsyncMethodCallStats(return_value=allowed)
        router.gather_sockets = AsyncMethodCallStats(return_value=sockets_ids)
        router.send_to = AsyncMethodCallStats(return_value=send_to_result)

        # A Socket with a simulated ID; to be matched later.
        websocket = MockWebSocket()
        websocket.socket_id = origin_socket_id
        # The _real_ message to send; should go to (1,2,4)
        msg = Envelope({'text': 'banana'}, 'owner')

        # Run the test. Applying the `roomcast` import here so it's easy
        # to find
        from porthouse.dispatch.roomcast import roomcast

        # Run it within the async loop. aka:
        # result = await roomcast(router, websocket, msg)
        coro = roomcast(router, websocket, msg)
        result = self.get_async_result(coro)

        # Assert the gather sockets only call what's allowed.
        assert router.gather_sockets.called_with(*allowed,
                                                origin_socket=origin_socket_id)
        # sends to the _given_ sockets
        assert router.send_to.called_with(sockets_ids, websocket, msg)

        # The result should be the routed value.
        assert result == send_to_result
```

Test an adapter `websocket_accept` function, using a mock websocket:

```py

from mocks import *
from asyncsupported_testcase import *

from porthouse.adapters.base import Adapter
from porthouse.router.router import Router


class TestAdapterBase(AsyncSupportedTestCase):
    """In this example we test the adapter for a good socket connection.
    It should call upon the token usage and perform 1 accept.
    """
    def setUp(self):
        """Standard setUp and teardown of the TestCase.
        """
        # Setup a router, with an _endpoint_ - The endpoint doesn't matter
        # as the MockTokens class doesn't perform a request.
        host_endpoint = 'fancy host endpoint'
        router = Router(host=host_endpoint)
        router._host = host_endpoint
        router._mount(host=host_endpoint)
        # The `Tokens()` routines are replaced with a MockTokens() instance.
        # This captures token calls.
        mt = MockTokens()
        router.tokens = mt
        # Ensure the IP Host rule has the same Tokens instance.
        # This is ugly though and will change.
        router.access_rules.rules[1].tokens = mt

        # Setup a standard adapter with a standard router.
        # The only mocked component is the `Tokens()` processor.
        adapter = Adapter(router)
        self.adapter = adapter

    def test_websocket_accept_good_token(self):
        """Assert the adapter accept function, runs the accept procedure.
            ok = await self.adapter.websocket_accept(1)
        """
        # Create a prepared websocket to capture _accept_ calls on it (by the adapter)
        client = MockWebSocket()

        # We need a 'valid' token - Luckily the MockRouter has one;.. "banana"
        tokens_unit = self.adapter.router.tokens
        token = tokens_unit.valid_token

        # _run_ the async function within the event loop.
        # akin to: await self.adapter.websocket_accept(client, token=token)
        coro = self.adapter.websocket_accept(client, token=token)
        accepted = self.get_async_result(coro)

        # The tokens should be called with the socket id.
        assert tokens_unit.use_token_called_with == (client.socket_id, token)
        # the client function should have been called: websocket.accept()
        assert client.accept_call_count == 1
        # A sucessfull onboarding return True
        assert accepted is True
```

Using a `MethodSink` (not `async`) in place of any function. In this case an `argparse` method:

```py
from unittest import TestCase

from mocks import MethodSink

from porthouse.arguments import installer


class TestArgumentsInstaller(TestCase):
    """Because we don't have any async code, we don't need `AsyncSupportedTestCase`
    """

    def test_apply_subparsers_collects_subparser(self):
        """Test the `argparse.Parser.add_subparsers` method was called
        when appling a new subparser through the installer.
        """
        # The `MethodSink` can replace all methods in an object.
        subparser = MethodSink()
        # And the return value from the (above) calls. are new sinks.
        # subparser.sub_method() == MockSink()
        subparser.add_parser.return_value = MethodSink()
        parser = MethodSink()
        #  And again. And call to any subparser will be captured in a sink.
        parser.add_subparsers.return_value = subparser

        # Execute as normal
        installer.apply_subparsers(parser)

        # Now check the deep sink, ensuring the add_subparsers was called
        # when we installed the new parser. in the `installer` through:
        # installer.apply_subparsers -> parser.add_subparsers -> subparser
        assert parser.add_subparsers.called == True
```