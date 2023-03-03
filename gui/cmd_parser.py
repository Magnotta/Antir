from classes.game import Game
from classes.time import Time

class Parser:
    def __init__(self) -> None:
        self.description = ''
        self.ans = ''
        self.parsed = []
        self.command_is_recognized: bool = False
        self.command_is_complete: bool = False

    def __init__(self, g: Game) -> None:
        self.time_dict = {'a': [g.advance,'time'],}
        self.env_dict = {}
        self.player_dict = {'h': [g.hunger, 'player', 'int'],
                            'b': [g.blood, 'player', 'int'],
                            'p': [g.pdr, 'player', 'int'],
                            's': [g.stamina, 'player', 'int']}
        self.location_dict = {'g': [g.move_scene, 'str']}

        self.top_dict = {'t': self.time_dict,
                        'p': self.player_dict,
                        'e': self.env_dict,
                        'l': self.location_dict}

    def parse(self, chars: str):
        if len(chars) < 2:
            self.command_is_recognized = False
            return

        top = chars[0]
        chars = chars[1:]
        low = chars[0]
        chars = chars[1:]

        try:
            func = self.top_dict[top][low][0]
        except KeyError:
            self.command_is_recognized = False
        else:
            self.command_is_recognized = True

        if not self.command_is_recognized:
            return
        
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
