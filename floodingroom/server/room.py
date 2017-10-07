import sys
import random


class RoomException(Exception):
    pass


class RoomOverflowException(RoomException):
    pass


class PlayerInRoomException(RoomException):
    pass


class GameStartedException(RoomException):
    pass


class MissedPlayerException(RoomException):
    pass


class BetOverflowException(RoomException):
    pass


class Room(object):
    def __init__(self, roomid, points_limit, players_limit, round_limit, bet_limit):
        self.id = roomid
        self.is_started = False
        self.points_limit = points_limit
        self.players_limit = players_limit
        self.round_limit = round_limit
        self.bet_limit = bet_limit
        self.total = 0
        self.round = 0
        self.players_bets = {}

    def start(self):
        self.is_started = True

    def add_player(self, sid):
        if sid in self.players_bets:
            PlayerInRoomException('{sid} already in room {roomid}'.format(sid=sid, roomid=self.id))
            return
        if self.is_full:
            raise RoomOverflowException('{roomid} room is full'.format(roomid=self.id))
        if self.is_started:
            raise GameStartedException('Game in {roomid} already started'.format(roomid=self.id))
        self.players_bets[sid] = None

    def add_bet(self, sid, points):
        if sid not in self.players_bets:
            raise MissedPlayerException('Bad {sid} for room {roomid}'.format(sid=sid, roomid=self.id))
        if points > self.bet_limit:
            raise BetOverflowException('{sid} makes too big bet, limit is {limit}'.format(sid=sid, limit=self.bet_limit))
        self.players_bets[sid] = points

    def add_random_bet(self, sid, a, b):
        if sid not in self.players_bets:
            raise MissedPlayerException('Bad {sid} for room {roomid}'.format(sid=sid, roomid=self.id))
        self.players_bets[sid] = random.randint(a, b)

    def end_round(self):
        self.round += 1
        for player, bet in self.players_bets.items():
            if not bet:
                self.add_random_bet(player, 0, self.bet_limit)

    @property
    def is_game_over(self):
        return self.total >= self.points_limit or self.round >= self.round_limit

    @property
    def is_full(self):
        return len(self.players_bets) >= self.players_limit
