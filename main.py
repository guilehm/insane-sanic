import os

from sanic import Sanic
from sanic.websocket import WebSocketProtocol

app = Sanic(__name__)
app.static('/', 'hello-world.html')

connections = set()

PORT = os.getenv('PORT', 8000)


async def broadcast(message):
    for conn in connections:
        await conn.send(message)


@app.websocket('/socket')
async def socket_route(request, ws):
    name = None
    connections.add(ws)
    try:
        name = await ws.recv()
        await broadcast(f'New user: {name}')
        while True:
            message = await ws.recv()
            await broadcast(f'{name} says: {message}')
    finally:
        connections.remove(ws)
        if name is not None:
            await broadcast(f'{name} lef the chat')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, protocol=WebSocketProtocol)
