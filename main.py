from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol

app = Sanic(__name__)
app.static('/', 'hello-world.html')


@app.websocket('/socket')
async def socket_route(request, ws):
    return json({"hello": "world"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)
