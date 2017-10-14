import uuid

import eventlet

from .room import Room


class RoomStorage(object):

    def __init__(self, max_rooms=1000):
        self.rooms = []
        self.max_rooms = max_rooms

    def add_player(self, sid):
        for room in self.rooms:
            if not room.is_full:
                return room.add_player(sid)
        if len(self.rooms) >= self.max_rooms:
            raise RuntimeError("rooms limit reached!")
        room = Room(
            roomid=uuid.uuid4().hex,
            players_limit=3,
            round_limit=3,
            target_level=0.75)
        room.semaphore = eventlet.Semaphore()
        self.rooms.append(room)
        print(f"new room spawned. now {len(self.rooms)} rooms")
        return room.add_player(sid)

    def get_room_with_player(self, sid):
        for room in self.rooms:
            if sid in room.players:
                return room

    def delete_room(self, room):
        self.rooms.remove(room)
