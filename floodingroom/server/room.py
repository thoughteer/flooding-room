import datetime
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


class PlayerException(RoomException):
    pass


class Player(object):
    class Type(object):
        evil = 'Bad person'
        good = 'Good person'

    def __init__(self, id, type, bet_limit):
        self.id = id
        self.type = type
        self.bet_limit = bet_limit
        self._bet = None

    @property
    def bet(self):
        if not self._bet:
            return random.randint(0, self.bet_limit)
        return self._bet

    @bet.setter
    def bet(self, points):
        if points > self.bet_limit:
            raise BetOverflowException('{id} makes too big bet, limit is {limit}'.format(id=id, limit=self.bet_limit))
        self._bet = points


class Room(object):
    def __init__(self, roomid, points_limit, players_limit, round_limit, bet_limit):
        self.timestamp = datetime.datetime.utcnow()
        self.id = roomid
        self.is_started = False
        self.points_limit = points_limit
        self.players_limit = players_limit
        self.round_limit = round_limit
        self.bet_limit = bet_limit
        self.total = 0
        self.round = 0
        self.players = {}
        self.pidors = get_pidors(players_limit)

    def get_player_type(self):
        if len(self.players) == self.pidors[-1]:
            self.pidors.pop()
            return Player.Type.evil
        return Player.Type.good

    def start(self):
        self.is_started = True

    def add_player(self, sid):
        if sid in self.players:
            raise PlayerInRoomException('{sid} already in room {roomid}'.format(sid=sid, roomid=self.id))
        if self.is_full:
            raise RoomOverflowException('{roomid} room is full'.format(roomid=self.id))
        if self.is_started:
            raise GameStartedException('Game in {roomid} already started'.format(roomid=self.id))

        self.players[sid] = Player(sid, self.get_player_type(), self.bet_limit)

    def add_bet(self, sid, points):
        if sid not in self.players:
            raise MissedPlayerException('Bad {sid} for room {roomid}'.format(sid=sid, roomid=self.id))
        self.players[sid].bet = points

    def end_round(self):
        self.round += 1
        self.total += sum([player.bet for id, player in self.players.items()])

    @property
    def is_game_over(self):
        return self.total >= self.points_limit or self.round >= self.round_limit

    @property
    def is_full(self):
        return len(self.players) >= self.players_limit


def get_pidors(number):
    num_pidors = number / 3
    indexes = []
    while num_pidors > 0:
        pidor = random.randint(0, number)
        if pidor not in indexes:
            indexes.append(pidor)
            num_pidors -= 1

    return list(reversed(sorted(indexes)))