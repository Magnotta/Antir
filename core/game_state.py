from systems.time_service import Time
from player.domain import Player


class GameState:
    def __init__(self, players: list[Player]):
        self.players = players
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

    def get_player_by_id(self, id: int) -> Player:
        for p in self.players:
            if p.player_rec.id == id:
                return p
        raise ValueError(f"Invalid player ID: {id}")

    def get_players_by_id(
        self, ids: list[int]
    ) -> list[Player]:
        filtered_players = filter(
            lambda player: player.player_rec.id in ids,
            self.players,
        )
        return list(filtered_players)
