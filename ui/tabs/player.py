from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
)
from player.domain import Player
from .single_player import SinglePlayerTab


class PlayersTab(QWidget):
    def __init__(self, player_domains: list[Player]):
        super().__init__()
        self.players = player_domains
        self.player_tabs: list[SinglePlayerTab] = []
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        for player in self.players:
            tab = SinglePlayerTab(player)
            self.player_tabs.append(tab)
            name = player.player_rec.name
            self.tabs.addTab(tab, name)

    def refresh(self):
        for tab in self.player_tabs:
            tab.refresh()
