from ..envelope import Envelope
from ..register import live_register
from .. import log


async def roomcast(router, websocket, msg:Envelope):
    # convert the rooms to socket names
    allowed = await router.filter_allowed_destinations(websocket, msg)
    log.d(f'Send to {allowed}')

    # Convert the room names to live sockets.
    sid = websocket.socket_id
    sockets = await router.gather_sockets(*allowed, origin_socket=sid)
    log.d(f'{len(sockets)} target sockets')

    # send to subscribed
    # return await router.supercast(websocket, msg)
    return await router.send_to(sockets, websocket, msg)
