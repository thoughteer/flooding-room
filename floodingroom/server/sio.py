import uuid

import flask
import flask_socketio

from .app import app
from .room import Room


class SIO(flask_socketio.SocketIO):

    def __init__(self):
        flask_socketio.SocketIO.__init__(self, app)
        self.room = None
        self.__configure()

    def __configure(self):

        @self.on("connect")
        def connect():
            print("connect ", flask.request.sid)

        @self.on("ready")
        def accept(json):
            if self.room is None or self.room.is_game_over:
                self.room = Room(roomid=uuid.uuid4().hex, points_limit=100, players_limit=10, round_limit=3)
            try:
                self.room.add_player(flask.request.sid)
            except Exception as exc:
                self.emit("decline", room=flask.request.sid, data={"reason": str(exc)})
            else:
                self.emit("accept", room=flask.request.sid, data={
                    "points_limit": self.room.points_limit,
                    "players_limit": self.room.players_limit,
                    "round_limit": self.room.round_limit,
                })

        @self.on("disconnect")
        def disconnect():
            print("disconnect ", flask.request.sid)


sio = SIO()
