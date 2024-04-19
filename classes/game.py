from .time import Time
from .event import Event, daily_events
from player.player import Player
from player.inventory import Inventory

class Game:
    def __init__(self, save_path=None, players: list[Player] =None, game_time=(0,0,0)) -> None:
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
        self.item_pool = Inventory(1000)
        self.parser = Parser(self)

    def start(self):
        for e in daily_events:
            self.game_events.append(e)

    def step(self):
        self.time += (0,0,1)

        for e in self.game_events:
            if e.due_time == self.time:
                self.parser.parse(e.action)
                self.execute(self.parser.parsed)
                self.game_events.remove(e)

        if self.time.hour_change:
            pass
        if self.time.day_change:
            self.game_events.append(Event((self.time.d, 12, 0), 'ph*1'))
            self.game_events.append(Event((self.time.d, 18, 0), 'ph*1'))
            self.game_events.append(Event((self.time.d, 23, 59), 'ph*1'))

    def execute(self, cmd):
        cmd[0](*cmd[1])

    def advance(self, mins):
        for i in range(mins):
            self.step()

    def blood(self, target: str, points: int):
        if target == '*':
            for p in self.players:
                p.takeBloodHit(points)
        else:
            player_id = int(target)
            if player_id < 1 or player_id > len(self.players):
                print(f'{player_id} is not a player')
                return
            self.players[player_id-1].takeBloodHit(points)
    
    def pdr(self, target: str, points: int):
        if target == '*':
            for p in self.players:
                p.takePDRHit(points)
        else:
            player_id = int(target)
            self.players[player_id].takePDRHit(points)

    def hunger(self, target: str, points: int):
        if target == '*':
            for p in self.players:
                p.addHunger(points)
        else:
            player_id = int(target)
            self.players[player_id].addHunger(points)

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
        self.description = ''
        self.ans = ''
        self.parsed = []
        self.command_is_recognized: bool = False
        self.command_is_complete: bool = False

        self.time_dict = {'a': [g.advance,'int'],}
        self.env_dict = {}
        self.player_dict = {'h': [g.hunger, 'player', 'int'],
                            'b': [g.blood, 'player', 'int'],
                            'p': [g.pdr, 'player', 'int'],
                            's': [g.stamina, 'player', 'int']}
        self.location_dict = {'g': [g.moveTo, 'str']}

        self.top_dict = {'t': self.time_dict,
                        'p': self.player_dict,
                        'e': self.env_dict,
                        'l': self.location_dict}

    def parse(self, chars: str):
        if len(chars) < 2:
            self.command_is_recognized = False
            return

        top, chars = chars[0], chars[1:]
        low, chars = chars[0], chars[1:]

        try:
            func = self.top_dict[top][low][0]
        except KeyError:
            self.command_is_recognized = False
            return
        else:
            self.command_is_recognized = True
        
        try:
            args = []
            for arg_type in self.top_dict[top][low][1:]:
                if arg_type == 'time':
                    arg_len = 0
                    buffer = ''
                    for char in chars:
                        if char.isdigit():
                            buffer += char
                            arg_len += 1
                        else:
                            break
                    chars = chars[arg_len:]
                    args.append(Time.from_int_mins(int(buffer)))
                elif arg_type == 'player':
                    args.append(chars[0])
                    chars = chars[1:]
                elif arg_type == 'int':
                    arg_len = 0
                    buffer = ''
                    for char in chars:
                        if char.isdigit() or char == '-':
                            buffer += char
                            arg_len += 1
                        else:
                            break
                    chars = chars[arg_len:]
                    args.append(int(buffer))
                elif arg_type == 'str':
                    arg_len = 0
                    buffer = ''
                    for char in chars:
                        arg_len += 1
                        buffer += char
                        if char == ';':
                            break
                    chars = chars[arg_len:]
                    args.append(buffer)
        except ValueError:
            self.command_is_complete = False
            return
        except IndexError:
            self.command_is_complete = False
            return
        else:
            self.command_is_complete = True


        self.parsed = func, args
