from PyQt6.QtWidgets import QApplication
import sys
from ui.window import Window
from db.database import init_metadata, init_db
from db.models import PlayerRecord
from db.repository import (
    EventRepository,
    ItemRepository,
    PlayerRepository,
    LocationRepository,
)
from player.domain import Player
from core.engine import Engine
from core.defs import BASE_PLAYER_STATS


if __name__ == "__main__":
    sys.tracebacklimit = 1
    db_eng, Session = init_metadata()
    session = Session()
    init_db(session)
    item_repo = ItemRepository(session)
    player_repo = PlayerRepository(session)
    event_repo = EventRepository(session)
    loc_repo = LocationRepository(session)
    player_recs = (
        session.query(PlayerRecord)
        .order_by(PlayerRecord.id)
        .all()
    )
    if not player_recs:
        raise RuntimeError("No players found in DB")
    players = []
    for player, player_stat_dict in zip(
        player_recs, BASE_PLAYER_STATS.items()
    ):
        players.append(
            Player(player, player_repo, item_repo)
        )
    engine = Engine(
        event_repo,
        item_repo,
        player_repo,
        loc_repo,
        players,
    )
    app = QApplication(sys.argv)
    win = Window(engine)
    win.show()
    sys.exit(app.exec())
