from sqlalchemy.orm import Session
from core.defs import BASE_PLAYER_ATTRIBUTES
from core.time import Time
from player.domain import Player
from db.repository.item import ItemRepository
from db.repository.location import LocationRepository
from db.repository.player import PlayerRepository
from db.repository.global_var import GlobalVarRepository
from db.models.world import Locality
from db.models.player_record import PlayerRecord
from db.database import init_globals, StateProperties


class StateProperty:
    def __init__(self, session: Session):
        self.var_repo = GlobalVarRepository(session)

    def __getitem__(self, key: str):
        return self.var_repo.get(key)

    def __setitem__(self, key: str, value):
        self.var_repo.set(key, value)


class GameState:
    def __init__(self, session: Session):
        self.item_repo = ItemRepository(session)
        self.player_repo = PlayerRepository(session)
        self.loc_repo = LocationRepository(session)
        self.globals = StateProperty(session)
        init_globals(session)
        self.time = Time(
            self.globals[
                StateProperties.LAST_SIMULATED_TICK
            ]
        )
        player_recs = (
            session.query(PlayerRecord)
            .order_by(PlayerRecord.id)
            .all()
        )
        if not player_recs:
            raise RuntimeError("No players found in DB")
        self.players: list[Player] = []
        for player, player_stat_dict in zip(
            player_recs, BASE_PLAYER_ATTRIBUTES.items()
        ):
            self.players.append(
                Player(
                    player, self.player_repo, self.item_repo
                )
            )
        self.locality: Locality = (
            self.loc_repo.get_locality_by_id(1)
        )

    def get_placedatetime_string(self):
        return f"{str(self.locality)}, {str(self.time)}"

    def get_player_by_id(self, id: int) -> Player:
        for p in self.players:
            if p.player_rec.id == id:
                return p
        raise ValueError(f"Invalid player ID: {id}")

    def update_time(self):
        """Updates the time entry in Global Vars table"""
        self.globals[
            StateProperties.LAST_SIMULATED_TICK
        ] = self.time.tick

    def next_event_tag(self) -> int:
        current = (
            self.globals[StateProperties.NEXT_EVENT_TAG] + 1
        )
        self.globals[StateProperties.NEXT_EVENT_TAG] = (
            current + 1
        )
        return current
