from collections import defaultdict

from loguru import logger
dlog = logger.debug


ROOMS = {
    'alpha': {
        'subscribers': {
            'user': {
                'permissions': {'read'}
            }
        }
    },
}


class SocketRoomBinding:
    rooms = None

    def __init__(self):
        self.rooms = set()


class Rooms(object):
    def __init__(self):
        self.open_rooms = {}
        self.SOCKETS = defaultdict(SocketRoomBinding)

    def socket_graph_add(self, sid, name):
        # socket_graph_add(sid, name)
        self.SOCKETS[sid].rooms.add(name)

    def socket_graph_remove(self, sid, name):
        # socket_graph_remove(sid, name)
        self.SOCKETS[sid].rooms.remove(name)

    def get(self, name):
        """Return a room instance
        """
        room = self.open_rooms.get(name)
        if room is None:
            room = Room(self, name)
        return room

    get_room = get

    async def remove_connection(self, socket_id):
        """Remove the socket id from active rooms.
        """
        # Careful. This socket id rooms may change size when iterating.
        for room_name in tuple(self.SOCKETS[socket_id].rooms):
            room = self.open_rooms.get(room_name)
            await room.remove_connection(socket_id=socket_id)
            # socket_graph_remove(sid, room_name)


class Room(object):
    """A live room instanve.
    """
    connections = None

    def __init__(self, space, name):
        self.connections = set()
        self.space = space
        self.name = name
        self.open = False

    async def add_connection(self, websocket):
        sid = websocket.socket_id
        self.connections.add(sid)
        l = len(self.connections)
        if self.open is False:
            self.open_room()
        self.space.socket_graph_add(sid, self.name)

        dlog(f'Assigning connection "{sid}" to {self.name} - len({l})')

    def open_room(self):
        """This room has become _active_ due to this first socket.
        Ensure the room exists persistently for all incoming
        connections and mark this user as the _owner_.
        """
        dlog(f'Opening new room "{self.name}" into space "{self.space}"')
        self.space.open_rooms[self.name] = self
        self.open = True

    async def remove_connection(self, websocket=None, socket_id=None):
        sid = socket_id or websocket.socket_id
        self.connections.remove(sid)
        l = len(self.connections)
        self.space.socket_graph_remove(sid, self.name)
        dlog(f'Removed connection "{sid}" from {self.name} - len({l})')

