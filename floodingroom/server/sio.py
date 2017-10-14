import datetime
import time

import flask
import flask_socketio

from .app import app
from .room_storage import RoomStorage


class SIO(flask_socketio.SocketIO):

    def __init__(self):
        flask_socketio.SocketIO.__init__(self, app, async_mode="eventlet")
        self.rooms = RoomStorage()
        self.__configure()

    def __configure(self):

        @self.on("connect")
        def connect():
            print("connect ", flask.request.sid)

        @self.on("ready")
        def accept(json):
            # get unique user id
            sid = flask.request.sid
            # try to add the player
            try:
                player = self.rooms.add_player(sid)
                room = player.room
                flask_socketio.join_room(room.id)
                print("client %s joined the room" % sid)
            except Exception as exc:
                flask_socketio.emit("decline", {"reason": str(exc)})
                return
            flask_socketio.emit("accept", {
                "points_limit": 1.0,
                "players_limit": room.players_limit,
                "round_limit": room.round_limit,
                "bet_limit": room.bet_limit,
                "player_count": len(room.players),
                "player_type": player.type,
                "players": repr(room.players),
            })

        @self.on("check")
        def check(json):
            sid = flask.request.sid
            room = self.rooms.get_room_with_player(sid)
            if room is None:
                return
            event = json["event"]
            print(f"checking event {event} for client {sid}")
            # TODO: dispatch properly
            if event == "start":
                # start if full or it's time to
                start_time = room.timestamp + 5
                now = time.perf_counter()
                if not room.is_full and now < start_time:
                    period = min(5, start_time - now)
                    print("ask client %s to hold for %f seconds" % (flask.request.sid, period))
                    flask_socketio.emit("hold", {"event": event, "period": period})
                    return
                print("start!")
                with room.semaphore:
                    if not room.is_started:
                        room.start_game()
                        flask_socketio.emit("start", {}, room=room.id, broadcast=True)
                return
            if event == "round":
                round_end_time = room.timestamp + 5
                now = time.perf_counter()
                if not room.are_all_bets_made and now < round_end_time:
                    period = min(5, round_end_time - now)
                    print("ask client %s to hold for %f seconds" % (flask.request.sid, period))
                    flask_socketio.emit("hold", {"event": event, "period": period})
                    return
                room.end_round()
                result = {"total": room.total}
                if room.is_game_over:
                    winners = room.end_game()
                    result["is_final"] = True
                    result["winners"] = winners
                else:
                    result["is_final"] = False
                flask_socketio.emit("round", result, room=room.id)
                if result["is_final"]:
                    with room.semaphore:
                        self.rooms.delete_room(room)
                return

        @self.on("bet")
        def bet(json):
            print(f"bet from {flask.request.sid}: {json['bet']}")
            room = self.rooms.get_room_with_player(flask.request.sid)
            room.add_bet(flask.request.sid, json["bet"])

        @self.on("disconnect")
        def disconnect():
            print("disconnect ", flask.request.sid)


sio = SIO()
