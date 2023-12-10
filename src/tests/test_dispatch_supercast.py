import runpy

from unittest.mock import patch
from mocks import *
from asyncsupported_testcase import *

from porthouse import register
from porthouse.envelope import Envelope

class TestDispatchSupercast(AsyncSupportedTestCase):
    # test that the supercast function
    def test_supercast(self):

        websocket = MockWebSocket()
        other_socket = MockWebSocket()
        another_socket = MockWebSocket()

        msg = Envelope({'text': 'banana'}, 'owner')
        custom_socket_id = '002939n2857v92835792735h92b75n2-75'

        websocket.socket_id = custom_socket_id

        register.CONNECTIONS['sockets'] = {
            custom_socket_id: websocket,
            'other_socket': other_socket,
            'another_socket': another_socket,
        }

        from porthouse.dispatch.supercast import supercast
        # 1. uses the socket id (by not calling the origin socket.)
        # No router required.
        coro = supercast(None, websocket, msg)
        self.get_async_result(coro)
        # 2. sends the message (text) to all live register sockets.
        assert websocket.send_text.called == False
        assert another_socket.send_text.called_with(msg.content['text'])
        assert other_socket.send_text.called_with(msg.content['text'])
        # 3. does not send the message to the origin pipe.
