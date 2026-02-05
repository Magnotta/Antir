from PyQt6.QtWidgets import QMainWindow, QTabWidget
from core.engine import Engine
from ui.home_tab import HomeTab
from ui.item_tab import ItemTab
from ui.player_tab import PlayersTab


class Window(QMainWindow):
    def __init__(
        self,
        session,
        engine: Engine,
        itemmold_repo,
        item_repo,
    ):
        super().__init__()
        self.setWindowTitle("Antir, otários")
        self.resize(800, 600)
        self.session = session
        self.engine = engine
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.home_tab = HomeTab(self.engine)
        self.item_tab = ItemTab(itemmold_repo, item_repo, self)
        self.player_tab = PlayersTab(engine.state.players)
        self.engine.signals.connect(
            "inventory", self.player_tab.refresh
        )
        self.engine.signals.connect(
            "equipment", self.player_tab.refresh
        )
        self.engine.signals.connect("stats", self.player_tab.refresh)
        self.engine.signals.connect("minute", self.home_tab.refresh)
        self.engine.signals.connect("location", self.home_tab.refresh)
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.item_tab, "Items")
        self.tabs.addTab(self.player_tab, "Players")
