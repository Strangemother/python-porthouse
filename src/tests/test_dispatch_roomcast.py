import runpy

from unittest.mock import patch
from mocks import *
from asyncsupported_testcase import *

from porthouse import register
from porthouse.envelope import Envelope

class TestDispatchRoomcast(AsyncSupportedTestCase):
    # test that the roomcast function
    #
    def test_roomcast(self):

        # filters for allows
        # sends the _allowed_ sockets.
        allowed = (1,2,4)
        origin_socket_id = '320f9j029jf 02'
        sockets_ids = ('A', 'B', 'C', origin_socket_id)
        send_to_result = {'some': 'result'}

        router = MockRouter()
        router.filter_allowed_destinations = AsyncMethodCallStats(return_value=allowed)
        router.gather_sockets = AsyncMethodCallStats(return_value=sockets_ids)
        router.send_to = AsyncMethodCallStats(return_value=send_to_result)

        websocket = MockWebSocket()
        websocket.socket_id = origin_socket_id

        msg = Envelope({'text': 'banana'}, 'owner')

        from porthouse.dispatch.roomcast import roomcast

        coro = roomcast(router, websocket, msg)
        result = self.get_async_result(coro)

        # Assert the gather sockets only call what's allowed.
        assert router.gather_sockets.called_with(*allowed,
                                                origin_socket=origin_socket_id)
        # sends to the _given_ sockets
        assert router.send_to.called_with(sockets_ids, websocket, msg)

        # The result should be the routed value.
        assert result == send_to_result