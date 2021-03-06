import datetime
import random
import time


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

    def __init__(self, id, type, bet_limit, room):
        self.id = id
        self.type = type
        self.bet_limit = bet_limit
        self._bet = None
        self.room = room

    def __repr__(self):
        return f"<{self.type} player {self.id}>"

    @property
    def bet(self):
        if not self._bet:
            return random.random() * self.bet_limit
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
    def __init__(self, bet_limit, room):
        super().__init__(self, self.Type.good, bet_limit, room)


class BadBot(Bot):
    def __init__(self, bet_limit, room):
        super().__init__(self, self.Type.evil, bet_limit, room)
        self._constant_bet = bet_limit if random.randint(0, 1) else 0

    @property
    def bet(self):
        return self._constant_bet


class Room(object):
    def __init__(self, roomid, players_limit, round_limit, target_level):
        self.timestamp = time.perf_counter()
        self.id = roomid
        self.is_started = False
        self.players_limit = players_limit
        self.round_limit = round_limit
        self.target_level = target_level
        self.total = 0
        self.round = 1
        self.players = {}
        pidor_count = random.randint(0, players_limit // 2)
        self.pidors = random.sample(range(players_limit), pidor_count)
        self.bet_limit = 2.0 * target_level / round_limit / (players_limit + (1 - target_level) * pidor_count)

    def get_next_player_type(self):
        if self.player_count in self.pidors:
            return Player.Type.evil
        return Player.Type.good

    def start_game(self):
        for _ in range(self.players_limit - self.player_count):
            if self.get_next_player_type() == Player.Type.good:
                bot = GoodBot(self.bet_limit, self)
            else:
                bot = BadBot(self.bet_limit, self)
            self.players[bot] = bot
        self.is_started = True
        self.timestamp = time.perf_counter()

    def add_player(self, sid):
        if sid in self.players:
            raise PlayerInRoomException('{sid} already in room {roomid}'.format(sid=sid, roomid=self.id))
        if self.is_started:
            raise GameStartedException('Game in {roomid} already started'.format(roomid=self.id))
        if self.is_full:
            raise RoomOverflowException('{roomid} room is full'.format(roomid=self.id))

        self.players[sid] = Player(sid, self.get_next_player_type(), self.bet_limit, self)
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
        self.timestamp = time.perf_counter()

    def end_game(self):
        if self.target_level <= self.total < 1:
            return "good"
        return "evil"

    def replace_with_bot(self, sid):
        if sid not in self.players:
            raise KeyError
        type = self.players[sid].type
        del self.players[sid]
        if type == Player.Type.good:
            bot = GoodBot(self.bet_limit, self)
        else:
            bot = BadBot(self.bet_limit, self)
        self.players[bot] = bot

    @property
    def are_all_bets_made(self):
        return all(player.is_bet_made for player in self.players.values())

    @property
    def is_game_over(self):
        return self.total >= 1 or self.round > self.round_limit

    @property
    def is_full(self):
        return len(self.players) >= self.players_limit

    @property
    def has_only_bots(self):
        return all(isinstance(player, Bot) for player in self.players.values())

    @property
    def player_count(self):
        return len(self.players)
