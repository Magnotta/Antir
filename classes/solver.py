from .game import Game
from .time import Time

class Solver:
    def __init__(self, g: Game) -> None:
        self.time_dict = {'m': [g.advance,'time'],}
        self.env_dict = {}
        self.player_dict = {}

        self.top_dict = {'t': self.time_dict,
                        'p': self.player_dict,
                        'e': self.env_dict,}

    def run_command(self, c: str, g: Game):
        top = c[0]
        c = c[1:]
        low = c[0]
        c = c[1:]
        func = self.top_dict[top][low][0]

        args = []
        for arg in self.top_dict[top][low][1:]:
            if arg == 'time':
                len = 0
                word = ''
                for char in c:
                    if char.isdigit():
                        word += char
                        len += 1
                    else:
                        break
                c = c[len:]
                args.append(Time.from_int_mins(int(word)))

        func(*args)