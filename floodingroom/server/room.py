import sys
import random


class Room(object):
    def __init__(self, roomid, limit, players_limit):
        self.id = roomid
        self.limit = limit
        self.players_limit = players_limit
        self.total = 0
        self.players_bets = {}

    def add_player(self, sid):
        if sid in self.players_bets:
            print('{sid} already in room {roomid}'.format(sid=sid, roomid=self.id), file=sys.stderr)
            return
        if len(self.players_bets) > self.players_limit:
            print('{roomid} room is full'.format(roomid=self.id), file=sys.stderr)
            return
        self.players_bets[sid] = None

    def add_bet(self, sid, points):
        if sid not in self.players_bets:
            print('Bad {sid} for room {roomid}'.format(sid=sid, roomid=self.id), file=sys.stderr)
            return
        self.players_bets[sid] = points

    def add_random_bet(self, sid, a, b):
        if sid not in self.players_bets:
            print('Bad {sid} for room {roomid}'.format(sid=sid, roomid=self.id), file=sys.stderr)
            return
        self.players_bets[sid] = random.randint(a, b)

    def end_round(self):
        for player, bet in self.players_bets.items():
            if not bet:
                self.add_random_bet(player, 0, 20)

        self.total += sum([v for k, v in self.players_bets.items()])
        if self.total >= self.limit:
            return True
        return False
