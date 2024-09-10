from classes.time import Time
from typing import Callable

class Event():
    def __init__(self, due_time: Time, action:str='', *, player_condition:Callable=None) -> None:
        self.due_time = due_time
        self.action = action
        self.player_condition = player_condition