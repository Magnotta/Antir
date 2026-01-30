from systems.time_service import Time

class GameState:
    def __init__(self):
        self.player_ids = list(range(5))
        self.time = Time()
        self.location = 'Dentro da consciência'

    @classmethod
    def from_dict(cls, data: dict):
        state = cls()
        state.time = data["tick"]
        state.location = data["location"]
        state.player = data["player"]
        return state
    
    def get_placedatetime_string(self):
        return f"{self.location}, {str(self.time)}"