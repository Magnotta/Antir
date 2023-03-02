from .time import Time
from .event import Event
from .player import Player

class Game:
    def __init__(self, save_path=None, players: list[Player] =None, game_time=(0,0,0)) -> None:
        self.save_path = save_path
        self.players = players
        self.time = Time(game_time)
        self.game_events: list[Event] = []
        self.daily_events = []
        self.location = ''

    def advance(self, adv: tuple):
        old_time = self.time
        new_time = old_time + adv

        for t in old_time.minutes_until(new_time):
            for e in self.game_events:
                if t == e.due_time:
                    #do that event!
                    pass

        self.time = new_time

        if new_time.d != old_time.d:
            # day change, update PDR, third hungerpt
            pass
        if new_time.h != old_time.h:
            # hour change, update hunger
            pass
        if new_time.m != old_time.m:
            # minute change, update bloodloss, stamina
            pass
    
    def hunger(self, target: str, points: int):
        if target == '*':
            for p in self.players:
                p.addHunger(points)
        else:
            player_id = int(target) - 1
            self.players[player_id].addHunger(points)

    def move_scene(self, location: str):
        self.location = location