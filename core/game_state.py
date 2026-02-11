from systems.time_service import Time
from player.domain import Player
from db.repository import (
    EventRepository,
    ItemRepository,
    PlayerRepository,
)


class GameState:
    def __init__(
        self,
        event_repo: EventRepository,
        item_repo: ItemRepository,
        player_repo: PlayerRepository,
        players: list[Player],
    ):
        self.players = players
        self.event_repo = event_repo
        self.item_repo = item_repo
        self.player_repo = player_repo
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
