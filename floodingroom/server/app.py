import uuid

import pkg_resources

import flask
import socketio

from .room import Room


sio = socketio.Server()

app = flask.Flask(__name__)
app.static_folder = pkg_resources.resource_filename("floodingroom", "server/resources")

room = None


@app.route("/")
def index():
    return app.send_static_file("index.html")


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)


@sio.on("ready")
def ready(sid, data):
    global room
    if room is None or room.is_game_over:
        room = Room(roomid=uuid.uuid4().hex, points_limit=100, players_limit=10, round_limit=3)
    try:
        room.add_player(sid)
    except Exception as exc:
        sio.emit("decline", room=sid, data={"reason": str(exc)})
    else:
        sio.emit("accept", room=sid, data={
            "points_limit": room.points_limit,
            "players_limit": room.players_limit,
            "round_limit": room.round_limit,
        })


@sio.on('chat message')
def message(sid, data):
    print("message ", data)
    sio.emit('reply', room=sid)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)
