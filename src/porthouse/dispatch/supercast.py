from ..envelope import Envelope
from ..register import live_register


async def supercast(router, websocket, msg:Envelope):
    """Dispatch the message to ALL live register connections
    """
    uuid = websocket.socket_id
    # for now, send to all.
    for k, socket in live_register.get_connections().items():
        if k == uuid:
            continue
        await socket.send_text(msg.content['text'])