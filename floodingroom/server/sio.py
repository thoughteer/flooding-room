import datetime
import uuid

import eventlet
import flask
import flask_socketio

from .app import app
from .room import Room


class SIO(flask_socketio.SocketIO):

    def __init__(self):
        flask_socketio.SocketIO.__init__(self, app, async_mode="eventlet")
        self.room = None
        self.room_semaphore = None
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
                    players_limit=2,
                    round_limit=3,
                    bet_limit=30)
                self.room_semaphore = eventlet.Semaphore()
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
                flask_socketio.emit("decline", {"reason": str(exc)})
                return
            flask_socketio.emit("accept", {
                "points_limit": self.room.points_limit,
                "players_limit": self.room.players_limit,
                "round_limit": self.room.round_limit,
                "bet_limit": self.room.bet_limit,
                "player_count": len(self.room.players),
                "player_type": player.type,
                "players": repr(self.room.players),
            })

        @self.on("check")
        def check(json):
            print("checking for client %s" % flask.request.sid)
            # start if full or it's time to
            start_time = self.room.timestamp + datetime.timedelta(seconds=30)
            now = datetime.datetime.utcnow()
            if not self.room.is_full and now < start_time:
                period = (start_time - now).total_seconds()
                print("ask client %s to hold for %f seconds" % (flask.request.sid, period))
                flask_socketio.emit("hold", {"period": period})
                return
            print("start!")
            with self.room_semaphore:
                if not self.room.is_started:
                    self.room.start()
                    flask_socketio.emit("start", {}, room=self.room.id, broadcast=True)

        @self.on("bet")
        def bet(json):
            print(f"bet from {flask.request.sid}: {json['bet']}")
            self.room.add_bet(flask.request.sid, json["bet"])

        @self.on("disconnect")
        def disconnect():
            print("disconnect ", flask.request.sid)


sio = SIO()
