"""The BackPipe

A Backpipe is a Router's dedicated connect to another router. Other
routers may connect to this backpipe for ferrying messages between peers.

The router created a pipe when the server is connected. If the backpipe connect
connect, it assumes no back connection.
"""
import asyncio
import uuid

from websockets import connect as w_connect
from websockets.exceptions import ConnectionClosedError

from . import config as conf

from loguru import logger
dlog = logger.debug


class BackPipeMixin(object):
    # Flagged True when applied by the async connect.
    has_backpipe = False
    backpipe_token = 9999

    def prepare_backpipe(self, host=None, ports=None):
        self.has_backpipe = True
        self._ports = ports or conf.BALANCE_PORTS
        self._host = host or conf.HOST
        dlog('prepare_backpipe: {ports}', ports=self._ports)
        self._pipe = BackPipe(self.backpipe_recv)

    async def start_backpipe(self, my_host=None, my_port=None):
        ports = self._ports or ()

        balance_address = (self._host, ports) # ('ip', (port, port,...))
        dlog(balance_address)
        balance_port = str(balance_address[1])


        if self.has_backpipe:
            self._pipe.set_router_address((my_host, my_port,))

        if my_port == balance_port:
            print('!! This is the balance port. No backpipe.')
            return

        if self.has_backpipe:
            await self.connect_backpipe(*balance_address)
        # await self.connect_backpipe(*balance_address, token)

    async def connect_backpipe(self, host, ports, token=None):
        uris = ()
        for port in ports:
            if token is None:
                token = self.get_backpipe_token(host,port)
            uri = 'ws://{}:{}/{}'.format(host, port, token)
            uris += (uri,)
        await self._pipe.connect_many(uris, listen=True)

    def get_backpipe_token(self, host,port):
        return self.backpipe_token

    async def backpipe_send(self, message):
        if self.has_backpipe:
            await self._pipe.send(message)
            return True
        dlog('No Backpipe.')
        return False

    async def backpipe_recv(self, message):
        dlog(f'RECV: "{message}"')


class BackPipe(object):
    """The `Backpipe` class is a self-contained bi-directional multiplex
    communications port, alloing a list of websockets _outbound_ from the "back"
    of the server.

    To initiate, provide a `response_handler` function, to accept messages into
    a controller:

        async def callback(message, socket):
            ...

        bp = Backpipe(callback)

    When prepared, call the `connect` method:

        uris = ["ws://..", "ws://..", ...]
        await bp.connect(uris, raise_disconnect=True)
    """
    def __init__(self, response_handler):
        # self.queue = asyncio.Queue()
        self.socket = None
        self.sockets = None

        self.response_handler = response_handler
        self.router_address = None

    # async def async_queue_put(self, data):
    #     return self.queue_put(data)

    # def queue_put(self, data):
    #     self.queue.put_nowait(data)

    async def close(self):
        for socket in (self.sockets or ()):
            if socket is None:
                continue
            await socket.close()
        await asyncio.sleep(0)  # yield control to the event loop

    def set_router_address(self, address:tuple):
        self.router_address = address

    async def connect(self, uri, raise_disconnect=False):
        return await self.connect_many(uri, raise_disconnect)

    async def connect_many(self, uris, raise_disconnect=False, listen=True):
        """Perform `connect_watch` for a list of uris.

            uris = ['ws://...', 'ws://...']
            self.connect_many(uris, raise_disconnect=False, listen=True)

        Is synonymous to:

            socket_1 = await self.connect_watch(uri[1], raise_disconnect, listen)
            socket_2 = await self.connect_watch(uri[2], raise_disconnect, listen)

        """
        dlog('Connecting to many backpipes', uris)
        sockets = ()
        for uri in uris:
            socket = await self.connect_watch(uri, raise_disconnect, listen)
            sockets += (socket,)
            # await self.producer_handler(self.socket)
        l = len(sockets)
        dlog("Prepared {c} socket{s}",
                c=l,
                s=['', 's'][int(l == 1)],
            )

        self.sockets = sockets
        return sockets

    async def connect_watch(self, uri, raise_disconnect=False, listen=True):
        """Connect to the given websocket `uri`. Dope the socket with a
        new socket_id and send a wake message. Finally create a new task to wait
        for new messages.

            socket = await self.connect_watch(uri, raise_disconnect=False, listen=True)

        Return the connected socket, whilst awaiting for messages.
        """
        try:
            socket = await w_connect(uri)
            _uuid = str(uuid.uuid4())
            socket.socket_id = _uuid
            dlog(f'Backpipe connected ({socket.port}): {uri}')
        except ConnectionRefusedError:
            dlog(f'Cannot connect to backpipe: {uri} - connection refused')
            return None

        await self.send_wake(socket)
        await asyncio.sleep(0)  # yield control to the event loop

        if listen:
            asyncio.create_task(self.consume_task(socket, raise_disconnect))
        return socket

    async def consume_task(self, socket, raise_disconnect=True):
        """The _consume_ method, setup as a `task` executor to list for incoming
        messages:

            asyncio.create_task(self.consume_task(socket, raise_disconnect=True))
        """
        try:
            await self.consume(socket)
        except ConnectionClosedError as exc:
            dlog('Backpipe closed:', exc)
            if socket:
                await socket.close()
            if raise_disconnect:
                raise exc

    async def consume(self, websocket):
        """Async wait upon the websocket for message. call `response_handler`
        for every message received.

        This method is async blocking. To circumvent this call the function as
        a new task

            asyncio.create_task(self.consume_task(socket, raise_disconnect))
        """
        async for message in websocket:
            dlog('BackPipe message from {id}', id=websocket.port)
            await self.response_handler(message, websocket)
            await asyncio.sleep(0)
            # await websocket.send('Thank you.')

    async def producer_handler(self, websocket):
        while True:
            message = await self.queue.get()
            await websocket.send(message)
            self.queue.task_done()
        dlog('Joining queue')
        await self.queue.join()

    async def send_wake(self, socket=None):
        """Send the _wake word_ as a message to the peer."""
        message = 'Hello from {}'.format(self.router_address)
        dlog('Sending wake word...')
        sent = await self.send(message, socket)
        dlog(f'{sent=}')

    async def send(self, data, socket=None):
        sock = socket or self.socket
        socks = self.sockets or [sock]
        sent = 0
        for _socket in socks:
            if _socket:
                await _socket.send(data)
                sent += 1

        if sent == 0:
            dlog('No Socket to send through')
            return False
        return True
