import datetime
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
            # create room if it doesn't exist yet or we're done
            if self.room is None or self.room.is_game_over:
                self.room = Room(
                    roomid=uuid.uuid4().hex,
                    points_limit=100,
                    players_limit=10,
                    round_limit=3,
                    bet_limit=30)
            roomid = self.room.id
            print("current room id: %s" % roomid)
            # get unique user id
            sid = flask.request.sid
            # try to add the player
            try:
                player = self.room.add_player(sid)
                flask_socketio.join_room(roomid)
                print("client %s joined the room" % sid)
            except Exception as exc:
                self.emit("decline", {"reason": str(exc)})
                return
            self.emit("accept", {
                "points_limit": self.room.points_limit,
                "players_limit": self.room.players_limit,
                "round_limit": self.room.round_limit,
                "bet_limit": self.room.bet_limit,
                "player_count": len(self.room.players),
                "player_type": player.type,
            })
            # start if full
            if len(self.room.players) == self.room.players_limit:
                print("room is full, start!")
                self.room.start()
                self.emit("start", {}, room=roomid, broadcast=True)
                return
            # wait for 30 seconds from room creation time
            start_time = self.room.timestamp + datetime.timedelta(seconds=30)
            now = datetime.datetime.utcnow()
            if now < start_time:
                print("sleeping")
                flask_socketio.sleep((start_time - now).total_seconds())
            # check whether the game has already started
            if not self.room.is_started:
                # start anyway
                self.room.start()
                self.emit("start", {}, room=roomid, broadcast=True)

        @self.on("disconnect")
        def disconnect():
            print("disconnect ", flask.request.sid)


sio = SIO()
