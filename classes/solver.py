from .game import Game
from .time import Time

class Solver:
    def __init__(self) -> None:
        pass

    def execute(self, exec_list: list):
        func = exec_list[0]
        args = exec_list[1]
        func(*args)