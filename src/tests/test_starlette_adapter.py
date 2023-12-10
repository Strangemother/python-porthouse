import runpy

from unittest.mock import patch
from mocks import *
from asyncsupported_testcase import *

from porthouse.adapters.starlette_adapter import StarletteAdapter
from porthouse.router.router import Router

class TestStarletteAdapter(AsyncSupportedTestCase):
    # def setUp(self):

    def get_mocked_adapter(self):
        router = MockRouter()
        sa = StarletteAdapter(router)
        return sa

    def get_mock_websocket(self):
        websocket = MockWebSocket()
        websocket.token = 'banana'
        websocket.socket_id = 'banana'
        return websocket

    def get_mock_pair(self):
        #sa, websocket = self.get_mock_pair()
        return (self.get_mocked_adapter(), self.get_mock_websocket(),)

    def get_mock_triple(self):
        return self.get_mock_pair() + (self.get_mock_data(),)

    def get_mock_data(self):
        data = {'some': 'data'}
        return data

    def test_generate_typemap(self):
        # Assert a dict complete with disconnect and default.
        res = StarletteAdapter({}).generate_typemap()
        assert isinstance(res, dict)
        # Each item is a function
        for key, func in res.items():
            assert callable(func)

    def test_handle_command_message(self):
        # Assert calls handle_message with the command function
        #return await self.handle_message(websocket, data, default=self.recv_socket_command)
        sa, websocket, data = self.get_mock_triple()
        # Insert an async stat sink
        sa.handle_message = AsyncMethodCallStats()

        coro = sa.handle_command_message(websocket, data)
        res = self.get_async_result(coro)

        default_func = sa.recv_socket_command

        assert sa.handle_message.called_with(websocket, data, default=default_func)

    def test_recv_socket_command_no_receipt(self):
        # async def recv_socket_command(self, websocket, data):
        sa, websocket, data = self.get_mock_triple()
        # router.recv_socket_event_return_result = None

        coro = sa.recv_socket_command(websocket, data)
        continue_value = self.get_async_result(coro)

        assert websocket.send_json.called == False
        assert continue_value == 1

    def test_recv_socket_command_with_receipt(self):
        # async def recv_socket_command(self, websocket, data):
        receipt = {'some': 'receipt'}
        sa, websocket, data = self.get_mock_triple()
        sa.router.recv_socket_event_return_result = receipt

        coro = sa.recv_socket_command(websocket, data)
        continue_value = self.get_async_result(coro)

        # assert if receipt, websocket.send_json is called.
        assert websocket.send_json.called_with({'receipt': receipt})
        # Assert return 1 (as continue)
        assert continue_value == 1

    def test_handle_message_default_func(self):
        ## async def handle_message(self, websocket, data, default=None):
        # It should capture the default if default is none
        # # call to the _type  within the data
        # return the return from the action function

        sa, websocket, data = self.get_mock_triple()

        ## Setup the default function to be called.
        expected_res = {'some': 'response'}
        action_func = AsyncMethodCallStats(return_value=expected_res)
        sa.typemap['default'] = action_func

        coro = sa.handle_message(websocket, data, default=None)
        action_func_result = self.get_async_result(coro)
        # Should have used the typemap[default] function
        assert action_func.called_with(websocket, data)
        assert action_func_result == expected_res

    def test_handle_message_typed_func(self):
        # It should capture the the custom typemap function
        sa, websocket, data = self.get_mock_triple()
        ## Setup the default function to be called.
        expected_res = {'eggs': 'response'}
        action_func = AsyncMethodCallStats(return_value=expected_res)
        sa.typemap['eggs'] = action_func
        data['type'] = 'eggs'

        coro = sa.handle_message(websocket, data, default=None)
        action_func_result = self.get_async_result(coro)
        # Should have used the typemap[default] function
        assert action_func.called_with(websocket, data)
        assert action_func_result == expected_res

    def test_default_action_no_receipt(self):
        # async def default_action(self, websocket, data):
        # calls recv_socket_event
        # is receipt, uses send_text
        sa, websocket, data = self.get_mock_triple()
        # sa.router.recv_socket_event_return_result = None
        sa.router.recv_socket_event = AsyncMethodCallStats()
        coro = sa.default_action(websocket, data)
        res = self.get_async_result(coro)

        assert sa.router.recv_socket_event.called_with(websocket, data)
        assert websocket.send_text.called == False
        assert res == 1

    def test_default_action_with_receipt(self):
        # async def default_action(self, websocket, data):
        sa, websocket, data = self.get_mock_triple()
        mock_receipt = {'eggs': 'response'}
        sa.router.recv_socket_event = AsyncMethodCallStats(return_value=mock_receipt)

        coro = sa.default_action(websocket, data)
        res = self.get_async_result(coro)

        assert sa.router.recv_socket_event.called_with(websocket, data)
        assert websocket.send_text.called_with(mock_receipt)
        assert res == 1

    def test_websocket_disconnect(self):
        # async def websocket_disconnect(self, websocket, data):
        sa, websocket, data = self.get_mock_triple()
        sa.router.websocket_disconnect = AsyncMethodCallStats()

        coro = sa.websocket_disconnect(websocket, data)
        res = self.get_async_result(coro)

        assert hasattr(websocket, '_ok')
        assert websocket._ok == 0
        assert res == 0
