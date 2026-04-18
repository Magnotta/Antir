from systems.time import Time
from player.domain import Player
from db.repository.item import ItemRepository
from db.repository.event import EventRepository
from db.repository.location import LocationRepository
from db.repository.player import PlayerRepository
from db.repository.global_var import GlobalVarRepository
from db.models.world import Locality
from db.database import init_time


class GameState:
    def __init__(
        self,
        event_repo: EventRepository,
        item_repo: ItemRepository,
        player_repo: PlayerRepository,
        loc_repo: LocationRepository,
        var_repo: GlobalVarRepository,
        players: list[Player],
    ):
        self.players = players
        self.event_repo = event_repo
        self.item_repo = item_repo
        self.player_repo = player_repo
        self.loc_repo = loc_repo
        self.var_repo = var_repo
        self.time = Time(init_time(player_repo.session))
        self.locality: Locality = (
            self.loc_repo.get_locality_by_id(1)
        )

    @classmethod
    def from_dict(cls, data: dict):
        state = cls()
        state.time = data["tick"]
        state.locality = data["locality"]
        state.player = data["player"]
        return state

    def get_placedatetime_string(self):
        return f"{str(self.locality)}, {str(self.time)}"

    def get_player_by_id(self, id: int) -> Player:
        for p in self.players:
            if p.player_rec.id == id:
                if not p.is_alive():
                    raise ValueError(
                        f"Player {id} is dead!"
                    )
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

    def update_time(self):
        """Updates the time entry in Global Vars table"""
        self.var_repo.update_time(self.time.tick)
