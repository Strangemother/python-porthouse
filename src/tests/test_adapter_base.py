import runpy

from mocks import *
from asyncsupported_testcase import *

from porthouse.adapters.base import Adapter
from porthouse.router.router import Router


class TestAdapterBase(AsyncSupportedTestCase):
    def setUp(self):
        host_endpoint = 'fancy host endpoint'
        router = Router(host=host_endpoint)
        router._host = host_endpoint
        router._mount(host=host_endpoint)
        mt = MockTokens()
        router.tokens = mt
        router.access_rules.rules[1].tokens = mt
        adapter = Adapter(router)
        self.adapter = adapter

    def test_websocket_accept_good_token(self):
        """Assert the adapter accept function, runs the accept procedure.

            ok = await self.adapter.websocket_accept(1)
        """
        client = MockWebSocket()
        tokens_unit = self.adapter.router.tokens
        token = tokens_unit.valid_token

        coro = self.adapter.websocket_accept(client, token=token)
        accepted = self.get_async_result(coro)

        # The tokens should be called with the socket id.
        assert tokens_unit.use_token_called_with == (client.socket_id, token)
        # the client function should have been called: websocket.accept()
        assert client.accept_call_count == 1
        # A sucessfull onboarding return True
        assert accepted is True

    def test_websocket_accept_bad_token(self):
        """Assert the adapter accept function does not accept a bad token.
        """
        client = MockWebSocket()
        tokens_unit = self.adapter.router.tokens
        token = tokens_unit.invalid_token

        coro = self.adapter.websocket_accept(client, token=token)
        accepted = self.get_async_result(coro)

        # A sucessfull onboarding return True
        assert accepted is False
        # will not have a socket_id
        assert hasattr(client, 'socket_id') is False
        # The accept() function is not called.
        assert client.accept_call_count == 0

    def test_websocket_wait_receive(self):
        """Call receive"""

        client = MockWebSocket()
        # tokens_unit = self.adapter.router.tokens
        # token = tokens_unit.invalid_token
        coro = self.adapter.wait_receive(client)
        accepted = self.get_async_result(coro)
        assert client.receive_call_count == 1

    def test_websocket_wait_exit_self_close_on_1(self):
        """Assert a connected self.close() is called upon wait_exit()"""

        client = MockWebSocket()
        client.client_state.value = 1 # websocket.CONNECTED
        inner_cache = {
            'call_count': 0
        }

        async def aclose(_self):
            inner_cache['call_count'] += 1

        self.adapter.close = aclose
        coro = self.adapter.wait_exit(client)
        accepted = self.get_async_result(coro)

        assert inner_cache['call_count'] == 1

    def test_websocket_wait_exit_on_state_1(self):
        """Assert a connected socket.close() is called upon wait_exit()"""

        client = MockWebSocket()
        client.client_state.value = 1 # websocket.CONNECTED

        coro = self.adapter.wait_exit(client)
        accepted = self.get_async_result(coro)

        assert client.close_call_count == 1

    def test_websocket_wait_exit_on_state_0(self):
        """Assert websocket.close() is not called when the socket is disconnected."""

        client = MockWebSocket()
        client.client_state.value = 0

        coro = self.adapter.wait_exit(client)
        accepted = self.get_async_result(coro)

        assert client.close_call_count == 0

    def test_websocket_wait_exit_on_state_1(self):
        """Assert a connected socket.close() is called upon wait_exit()"""

        client = MockWebSocket()

        coro = self.adapter.wait_receive_json(client)
        accepted = self.get_async_result(coro)

        assert client.receive_json_call_count == 1

    def test_close(self):
        client = MockWebSocket()
        coro = self.adapter.close(client)
        accepted = self.get_async_result(coro)

        assert client.close_call_count == 1

    def test_validate_accept(self):
        router = MockRouter()
        adapter = Adapter(router)
        router.access_rules = MethodSink()
        router.access_rules.is_valid.return_value = 101
        client = MockWebSocket()

        rule_is_valid = adapter.validate_accept(client)

        assert rule_is_valid == 101
        assert router.access_rules.is_valid.call_count == 1

    def test_handle_command_message(self):
        router = MockRouter()
        adapter = Adapter(router)

        client = MockWebSocket()
        client.token = 'banana'
        client.socket_id = 'banana'

        data = {}

        coro = adapter.handle_command_message(client, data)
        accepted = self.get_async_result(coro)

        router = adapter.router
        assert router.recv_socket_event_call_count == 1
        assert router.recv_socket_event_args == (client, data)

    def test_handle_command_message(self):
        router = MockRouter()
        adapter = Adapter(router)

        client = MockWebSocket()
        client.token = 'banana'
        client.socket_id = 'banana'

        data = {}

        coro = adapter.handle_command_message(client, data)
        accepted = self.get_async_result(coro)
        router = adapter.router

        # one call to the recv_socket_event
        assert router.recv_socket_event_call_count == 1
        assert router.recv_socket_event_args == (client, data)


    def test_default_action_no_receipt_return(self):
        router = MockRouter()
        router.recv_socket_event_return_result = None
        adapter = Adapter(router)

        client = MockWebSocket()
        client.token = 'banana'
        client.socket_id = 'banana'

        data = {}

        coro = adapter.default_action(client, data)
        accepted = self.get_async_result(coro)

        # No calls to send_text because the receipt is None.
        assert client.send_text_call_count == 0


    def test_default_action_receipt_return(self):
        router = MockRouter()
        router.recv_socket_event_return_result = 'receipt'
        adapter = Adapter(router)

        client = MockWebSocket()
        client.token = 'banana'
        client.socket_id = 'banana'

        data = {}

        coro = adapter.default_action(client, data)
        accepted = self.get_async_result(coro)

        assert client.send_text_call_count == 1
        assert client.send_text_args == ('receipt',)
