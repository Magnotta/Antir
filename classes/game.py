from .time import Time
from .event import Event_Engine
from player.player import Player
from player.inventory import Inventory

''''''

class Game:
    def __init__(self, save_path=None, players: list[Player]=None, game_time=(0,0,0)) -> None:
        """!
        @brief Game instance class, keeps all game information and provides an interface to edit it

        Parameters : 
            @param self => [description]
            @param save_path = None => [description]
            @param players : list[Player] = None => [description]
            @param game_time = (0,0,0) => [description]
        Retour de la fonction : 
            @return None => [description]

        """
        self.save_path = save_path
        self.players = players
        self.time = Time(game_time)
        self.location = ''
        self.item_pool = Inventory(666)
        self.ee = Event_Engine(self)

    def step(self):
        self.time += (0,0,1)
        self.ee.update()

    def execute(self, cmd_target_type, func, cmd_target_list, args_list):
        if cmd_target_type in ['Player',]:
            for target in cmd_target_list:
                func(target, *args_list)
        elif cmd_target_type in ['Tempo',]:
            func(*args_list)

    def hunger_all(self):
        for p in self.players:
            p.addHunger(1)

    def cmd_advance_minutes(self, mins):
        for _ in range(mins):
            self.step()

    def cmd_advance_hours(self, hours):
        for _ in range(60*hours):
            self.step()

    def cmd_blood(self, targets, points: int):
        for player_id in targets:
            self.players[player_id].takeBloodHit(points)
    
    def cmd_pdr(self, target: str, points: int):
        if target == '*':
            for p in self.players:
                p.takePDRHit(points)
        else:
            player_id = int(target)
            self.players[player_id].takePDRHit(points)

    def cmd_hunger(self, target, points: int):
        self.players[target].addHunger(points)

    def cmd_stamina(self, target: str, points: int):
        if target == '*':
            for p in self.players:
                p.takeStmHit(points)
        else:
            player_id = int(target)
            self.players[player_id].takeStmHit(points)

    def cmd_sleep(self, target):
        self.players[target].sleep()

    def cmd_move_scene_to(self, location: str):
        self.location = location
