from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)
from ..widgets.body import BodyWidget
from ..widgets.stats_panel import StatsPanel
from ..widgets.inventory_panel import InventoryPanel
from player.domain import Player


class SinglePlayerTab(QWidget):
    def __init__(self, player_domain: Player):
        super().__init__()
        self.player = player_domain
        self.stats_panel = StatsPanel(self.player.stats)
        self.inventory_panel = InventoryPanel(
            self.player.inventory
        )
        self.body = BodyWidget(
            self.player.player_rec.id,
            self.player.anatomy.repo,
        )
        layout = QHBoxLayout()
        layout.addWidget(self.body, stretch=1)
        layout.addWidget(self.stats_panel, stretch=1)
        layout.addWidget(self.inventory_panel, stretch=2)
        self.setLayout(layout)

    def refresh(self):
        self.stats_panel.refresh(self.player.stats)
        self.inventory_panel.refresh()

    def anatomical_update(self):
        self.body.paintEvent()
