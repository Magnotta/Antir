from .time import Time
from .event import Event
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
        self.game_events: list[Event] = []
        self.location = ''
        self.item_pool = Inventory(666)
        self.parser = Parser(self)

    def start(self):
        self.game_events.append(Event((self.time.d, 12, 0), 'ph*1'))
        # self.game_events.append(Event((self.time.d, 18, 0), 'ph*1'))
        # self.game_events.append(Event((self.time.d, 23, 59), 'ph*1'))

    def step(self):
        self.time += (0,0,1)

        for e in self.game_events:
            if e.due_time == self.time:
                self.parser.parse(e.action)
                self.execute(self.parser.exec)
                self.game_events.remove(e)

        if self.time.hour_change():
            pass
        if self.time.day_change():
            self.game_events.append(Event((self.time.d, 12, 0), 'ph*1'))
            self.game_events.append(Event((self.time.d, 18, 0), 'ph*1'))
            #self.game_events.append(Event((self.time.d, 23, 59), 'ph*1'))

            for p in self.players:
                p.step_pneuma()

    def execute(self, cmd_target_type, func, cmd_target_list, args_list):
        if cmd_target_type in ['Player',]:
            for target in cmd_target_list:
                func(target, *args_list)
        elif cmd_target_type in ['Tempo',]:
            func(*args_list)

    def advance_minutes(self, mins):
        for _ in range(mins):
            self.step()

    def advance_hours(self, hours):
        for _ in range(60*hours):
            self.step()

    def blood(self, targets, points: int):
        for player_id in targets:
            self.players[player_id].takeBloodHit(points)
    
    def pdr(self, target: str, points: int):
        if target == '*':
            for p in self.players:
                p.takePDRHit(points)
        else:
            player_id = int(target)
            self.players[player_id].takePDRHit(points)

    def hunger(self, target, points: int):
        self.players[target].addHunger(points)

    def stamina(self, target: str, points: int):
        if target == '*':
            for p in self.players:
                p.takeStmHit(points)
        else:
            player_id = int(target)
            self.players[player_id].takeStmHit(points)

    def moveTo(self, location: str):
        self.location = location

################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################

class Parser:
    def __init__(self, g: Game) -> None:
        self.ans = ''

        self.command_is_recognized: bool = False
        self.command_is_complete: bool = False

        """
        {'callable': ,
                                'handle': '',
                                'arg_types_list': []}
        """

        self.time_dict = {'m': {'callable':g.advance_minutes,
                                'handle':'Avançar Minutos',
                                'arg_types_list':['int']}}
        self.env_dict = {}
        self.player_dict = {'h': {'callable': g.hunger,
                                'handle': 'Esfoemar',
                                'arg_types_list': ['int']},
                            'b': {'callable': g.blood,
                                'handle': 'Dessangrar',
                                'arg_types_list': ['int']},
                            'p': {'callable': g.pdr,
                                'handle': 'Murchar',
                                'arg_types_list': ['int']},
                            's': {'callable': g.stamina,
                                'handle': 'Fatigar',
                                'arg_types_list': ['int']}}
        self.location_dict = {'g': {'callable': g.moveTo,
                                'handle': 'Mover',
                                'arg_types_list': ['str']}}

        self.base_dict = {'t': {'func_dict': self.time_dict,
                                'target_type': 'Tempo'},
                        'p': {'func_dict': self.player_dict,
                              'target_type': 'Player'},
                        'e': {'func_dict': self.env_dict,
                              'target_type': 'Ambiente'},
                        'l': {'func_dict': self.location_dict,
                              'target_type': 'Local'}}
        
    def parse(self, chars: str):
        if not chars:
            self.ans = ""
            return None # no input

        self.tokens = list(filter(None, chars.split(' ')))

        cmd_key = self.tokens[0]
        self.tokens.remove(cmd_key)

        if cmd_key[0] not in self.base_dict:
            self.ans = f"Primeiro char errado. Opções:\n{' '.join(self.base_dict.keys())}"
            return None # wrong first character
        
        if len(cmd_key) < 2:
            self.ans = f"Comandos de {self.base_dict[cmd_key[0]]['target_type']}:\n{' '.join(self.base_dict[cmd_key[0]]['func_dict'].keys())}"
            return None # command keyword incomplete
        
        try:
            func_dict = self.base_dict[cmd_key[0]]['func_dict'][cmd_key[1:]]
        except KeyError:
            self.ans = f"Comando errado. Opções de {self.base_dict[cmd_key[0]]['target_type']}:\n{' '.join(self.base_dict[cmd_key[0]]['func_dict'].keys())}"
            return None # wrong second character

        if len(self.tokens) < len(func_dict['arg_types_list']):
            self.ans = f"Argumentos de {func_dict['handle']}: alvos {' '.join(func_dict['arg_types_list'])}"
            return None
        
        cmd_target_list = self.read_target(self.base_dict[cmd_key[0]]['target_type'], self.tokens[0])

        args_list = []
        for idx, token in enumerate(self.tokens):
            args_list.append(getattr(self, f"read_arg_{func_dict['arg_types_list'][idx]}")(token))

        if len(func_dict['arg_types_list']) == len(args_list):
            self.ans = "Comando Completo."
        
        return (self.base_dict[cmd_key[0]]['target_type'], func_dict['callable'], cmd_target_list, args_list)

    def read_target(self, cmd_target_type, token):
        cmd_target_list = []
        if cmd_target_type == "Player":
            if token == '*':
                [cmd_target_list.append(x) for x in range(6)]
                self.tokens.remove(token)
            else:
                for char in token:
                    if char in ['0', '1', '2', '3', '4', '5']:
                        cmd_target_list.append(int(char))
                    else:
                        raise(TypeError)
                self.tokens.remove(token)
        elif cmd_target_type == "Item":
            cmd_target_list.append(int(token))
            self.tokens.remove(token)
        elif cmd_target_type == "Tempo":
            pass
        return cmd_target_list
                    
    def read_arg_player(self, token):
        pass

    def read_arg_time(self, token):
        pass

    def read_arg_int(self, token):
        return int(token)

    def read_arg_item(self, token):
        pass

    def read_arg_str(self, token):
        pass
