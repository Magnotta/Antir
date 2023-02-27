from ..classes.time import Time

class Event():
    def __init__(self, _due_time: Time, _daily: bool=False, action: callable=None) -> None:
        self.due_time = _due_time
        self.daily = _daily
        self.action = None
