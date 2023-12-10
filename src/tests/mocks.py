from functools import partial
from collections import defaultdict


class MethodCallStats(object):
    call_count = 0
    called = False
    calls = ()
    return_value = None

    def __init__(self, name, return_value=None):
        self._method_name = name
        self.return_value = return_value

    def __call__(self, *a, **kw):
        print('--- New Call to', self._method_name)
        self.call_count += 1
        self.called = True
        self.calls += ((a, kw),)
        return self.return_value

    def called_with(self, *a, **kw):
        """Assert if the given arguments match one of the calls.
        return bool.
        """

        for ca, ckw in self.calls:
            if (ca == a) and (ckw == ckw):
                return True
        return False

class MethodSink(MethodCallStats):
    """A simplified mocking utility, allowing the replacement of methods
    to capture call stats. Used in place of a regular Mock or MagicMock, allowing
    usage within an async environment.

        router = Router()
        router.access_rules = MethodSink()
        router.access_rules.is_valid.return_value = 101

        client = MockWebSocket()
        rule_is_valid = adapter.validate_accept(client)

        assert rule_is_valid == 101
        assert router.access_rules.is_valid.call_count == 1

    A `return_factory` is a functional call for a `return_value`. This can
    return a MethodSink()

        parser = MethodSink(return_factory=MethodSink)
        parser.subparser.submethod('cake')
        assert parser.subparser.submethod.call_count == 1

    This can be nested, allowing a `deep_sink` of methods.

    Here we have a parser, that returns a subparser when called.
    The subparser has a method `add_parser`, that returns a complex object.
    In each case we can _sink_ until all are manually mocked:

        subparser = MethodSink()
        subparser.add_parser.return_value = MethodSink()
        parser = MethodSink()
        parser.add_subparsers.return_value = subparser

    With `deep_sink=True` all subcalls of a `MethodSink` return a MethodSink:

        # same as above
        parser = MethodSink(return_factory=MethodSink, deep_sink=True)

    Notice the `return_factory` instead of a `return_value`, as this ensures
    a fresh `MethodSink` is _called_ rather than returning the same instance.
    """
    def __init__(self, return_factory=None, return_value=None, deep_sink=False):
        self.info = {}
        self.return_factory = return_factory or self.generic_return_factory
        self.return_value = return_value
        self.deep_sink = deep_sink

    def generic_return_factory(self):
        return self.return_value

    def __getattr__(self, name):
        print('\n--- GetAttr MethodSink', name)
        res = self.info.get(name, None) or None
        if res is None:
            u = self.return_factory()
            if self.deep_sink and isinstance(u, MethodSink):
                u.return_factory = self.return_factory
            res = MethodCallStats(name, return_value=u )
            self.info[name] = res
        return res
        # router.access_rules.is_valid.call_count == 1


class MockRouter(object):

    recv_socket_event_call_count = 0
    recv_socket_event_args = None
    recv_socket_event_return_result = None

    async def websocket_accept(self, websocket, **extras):
        return websocket, extras

    async def recv_socket_event(self, websocket, data):
        self.recv_socket_event_call_count += 1
        self.recv_socket_event_args = (websocket, data)
        return self.recv_socket_event_return_result


class MockClient(object):
    host = 'fancy host endpoint'


class MockClientState(object):
    value = -1


class MockWebSocket(object):
    def __init__(self):
        self.client = self._new_client()
        self.accept_call_count = 0
        self.receive_call_count = 0
        self.close_call_count = 0
        self.receive_json_call_count = 0
        self.send_text_call_count = 0
        self.client_state = MockClientState()
        self.validate_accept_call_count = 0

    def _new_client(self):
        return MockClient()

    async def accept(self):
        self.accept_call_count += 1

    async def receive(self):
        self.receive_call_count += 1

    async def close(self):
        self.close_call_count += 1

    async def receive_json(self):
        self.receive_json_call_count += 1

    async def send_text(self, content):
        self.send_text_call_count += 1
        self.send_text_args = (content,)


class MockTokens(object):

    def __init__(self):
        self.post_token = {}
        self.valid_token = 'banana'
        # any chars
        self.invalid_token = '23oij52oi3rjf09cj09'
        self.use_token_called_with = None

    async def exists(self, value):
        self.exists_called_with = (value,)
        return True

    async def use_token(self, socket_id, token):
        self.use_token_called_with = (socket_id, token,)
        return token == self.valid_token

    async def get_token_object(self, token):
        return {}