EVENTS = {}

class Event:
    type: str = "base"

    def __init__(self, payload: dict | None = None, due_tick: int = 0):
        self.payload = payload or {}
        self.due_tick = due_tick

    def apply(self, state):
        raise NotImplementedError

    def follow_up(self, state) -> list["Event"]:
        return []