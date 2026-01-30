from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QWidget
)
from player.domain import PlayerDomain
from ui.home_tab import HomeTab
from ui.item_tab import ItemTab
from ui.player_tab import PlayersTab

class Window(QMainWindow):
    def __init__(self, session, engine, player_domains):
        super().__init__()

        self.setWindowTitle("Antir, otários")
        self.resize(800, 600)

        self.session = session
        self.engine = engine

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tabs
        self.home_tab = HomeTab(self.engine)
        self.item_tab = ItemTab(s=session)
        self.player_tab = PlayersTab(player_domains)

        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.item_tab, "Items")
        self.tabs.addTab(self.player_tab, "Players")