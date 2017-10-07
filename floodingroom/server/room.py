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
        evil = 'evil'
        good = 'good'

    def __init__(self, id, type, bet_limit):
        self.id = id
        self.type = type
        self.bet_limit = bet_limit
        self._bet = None

    def __repr__(self):
        return f"<{self.type} player {self.id}>"

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

    @property
    def is_bet_made(self):
        return self._bet is not None

    def clear_bet(self):
        self._bet = None


class Bot(Player):

    @property
    def is_bet_made(self):
        return True


class GoodBot(Bot):
    def __init__(self, bet_limit):
        super().__init__(self, self.Type.good, bet_limit)


class BadBot(Bot):
    def __init__(self, bet_limit):
        super().__init__(self, self.Type.evil, bet_limit)
        self._constant_bet = bet_limit if random.randint(0, 1) else 0

    @property
    def bet(self):
        return self._constant_bet


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
        self.pidors = random.sample(range(players_limit), players_limit // 3)

    def get_next_player_type(self):
        if self.player_count in self.pidors:
            return Player.Type.evil
        return Player.Type.good

    def start(self):
        for _ in range(self.players_limit - self.player_count):
            if self.get_next_player_type() == Player.Type.good:
                bot = GoodBot(self.bet_limit)
            else:
                bot = BadBot(self.bet_limit)
            self.players[bot] = bot
        self.is_started = True

    def add_player(self, sid):
        if sid in self.players:
            raise PlayerInRoomException('{sid} already in room {roomid}'.format(sid=sid, roomid=self.id))
        if self.is_started:
            raise GameStartedException('Game in {roomid} already started'.format(roomid=self.id))
        if self.is_full:
            raise RoomOverflowException('{roomid} room is full'.format(roomid=self.id))

        self.players[sid] = Player(sid, self.get_next_player_type(), self.bet_limit)
        return self.players[sid]

    def add_bet(self, sid, points):
        if sid not in self.players:
            raise MissedPlayerException('Bad {sid} for room {roomid}'.format(sid=sid, roomid=self.id))
        self.players[sid].bet = points

    def end_round(self):
        self.round += 1
        self.total += sum(player.bet for player in self.players.values())
        for player in self.players.values():
            player.clear_bet()

    def end_game(self):
        balance = 100.0 - self.total * 100.0 / self.points_limit
        if 0 < balance < 20.0:
            return "Good persons win"
        return "Bad persons win"

    @property
    def are_all_bets_made(self):
        return all(player.is_bet_made for player in self.players.values())

    @property
    def is_game_over(self):
        return self.total >= self.points_limit or self.round >= self.round_limit

    @property
    def is_full(self):
        return len(self.players) >= self.players_limit

    @property
    def player_count(self):
        return len(self.players)
