from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol

app = Sanic(__name__)
app.static('/', 'hello-world.html')

connections = set()


@app.websocket('/socket')
async def socket_route(request, ws):
    name = None
    connections.add(ws)
    try:
        name = await ws.recv()
        for conn in connections:
            await conn.send(f'New user: {name}')
        while True:
            message = await ws.recv()
            for conn in connections:
                await conn.send(message)
    finally:
        connections.remove(ws)
        if name is not None:
            for conn in connections:
                await conn.send(f'{name} lef the chat')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)
