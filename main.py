import sys

from db.database import init_metadata, init_db
from db.models import PlayerRecord
from db.repository import (
    ItemRepository,
    PlayerStatRepository,
)
from player.domain import Player
from core.engine import Engine
from core.defs import BASE_PLAYER_STATS


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from ui.window import Window
    import sys

    db_eng, Session = init_metadata()
    session = Session()
    item_repo = ItemRepository(session)
    stat_repo = PlayerStatRepository(session)
    # loc_repo = LocationRepository(session)
    init_db(session)

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
        players.append(Player(player, item_repo, stat_repo))

    engine = Engine(session, players)
    app = QApplication(sys.argv)
    win = Window(session, engine)
    win.show()
    sys.exit(app.exec())
