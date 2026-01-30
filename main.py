import sys

from db.database import init_metadata, init_db, Session
from db.models import Player
from db.repository import ItemRepository
from player.domain import PlayerDomain
from ui.player_tab import PlayersTab
from ui.item_tab import ItemTab
from ui.home_tab import HomeTab
from core.engine import Engine



if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from ui.window import Window
    import sys

    init_metadata()
    session = Session()
    engine = Engine()
    item_repo = ItemRepository(session)
    init_db(session)

    players = session.query(Player).order_by(Player.id).all()
    if not players:
        raise RuntimeError("No players found in DB")
    
    player_domains = [
        PlayerDomain(player, item_repo)
        for player in players
    ]

    app = QApplication(sys.argv)
    win = Window(session, engine, player_domains)
    win.show()
    sys.exit(app.exec())