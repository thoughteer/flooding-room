import eventlet
import socketio

from floodingroom.server.app import app
from floodingroom.server.app import sio


if __name__ == "__main__":
    middleware = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(("", 8080)), middleware)
