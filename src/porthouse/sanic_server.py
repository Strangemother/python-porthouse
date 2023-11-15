from sanic import Sanic
from sanic import Request, Websocket
from sanic.response import text

from porthouse import primary

app = Sanic("MyHelloWorldApp")

@app.get("/")
async def hello_world(request):
    return text("Hello, world.")


@app.websocket("/<token:strorempty>")
async def feed(request: Request, ws: Websocket, token: str):
    ws._ok = await primary.router.websocket_accept(ws, token=token)

    # await primary.primary_ingress(websocket, token=token)
    async for msg in ws:
        await ws.send(msg)
        ok = await primary.handle_message(ws, { 'type': 'websocket.receive', 'text': msg})
