from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLabel,
    QGroupBox, QTableView, QVBoxLayout,
    QHBoxLayout, QTabWidget
)
from player.domain import Player
from player.stats import Stats

class InventoryTableModel(QAbstractTableModel):
    HEADERS = ["ID", "Name", "Type", "Location"]

    def __init__(self, items):
        super().__init__()
        self.items = items

    def rowCount(self, parent=None):
        return len(self.items)

    def columnCount(self, parent=None):
        return len(self.HEADERS)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        item = self.items[index.row()]
        col = index.column()
        if col == 0:
            return item.id
        if col == 1:
            return item.mold.name if hasattr(item, "mold") else str(item.original_mold)
        if col == 2:
            return item.mold.type if hasattr(item, "mold") else ""
        if col == 3:
            return self._location_text(item)

    def _location_text(self, item):
        if item.container_item_id:
            return "Container"
        return "Loose"
    

    
class InventoryPanel(QWidget):
    def __init__(self, inventory):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        title = QLabel("Inventory")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)
        self.table = QTableView()
        layout.addWidget(self.table)
        self.inventory = inventory
        self.refresh()

    def refresh(self):
        items = self.inventory.loose_items()
        self.model = InventoryTableModel(items)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()


    
class StatsPanel(QGroupBox):
    def __init__(self, stats:Stats):
        super().__init__("Stats")
        layout = QFormLayout()
        self.setLayout(layout)
        self.labels = {}
        for name, val in stats.get_all().items():
            label = QLabel(str(val))
            layout.addRow(name.replace("_", " ").title(), label)
            self.labels[name] = label

    def refresh(self, stats: Stats):
        for name, label in self.labels.items():
            label.setText(str(stats.get_all()[name]))



class SinglePlayerTab(QWidget):
    def __init__(self, player_domain: Player):
        super().__init__()
        self.player = player_domain
        self.stats_panel = StatsPanel(self.player.stats)
        self.inventory_panel = InventoryPanel(self.player.inventory)
        layout = QHBoxLayout()
        layout.addWidget(self.stats_panel, stretch=1)
        layout.addWidget(self.inventory_panel, stretch=2)
        self.setLayout(layout)

    def refresh(self):
        self.stats_panel.refresh(self.player.stats)
        self.inventory_panel.refresh()



class PlayersTab(QWidget):
    def __init__(self, player_domains: list[Player]):
        super().__init__()
        self.player_domains = player_domains
        self.player_tabs: list[SinglePlayerTab] = []
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        for domain in self.player_domains:
            tab = SinglePlayerTab(domain)
            self.player_tabs.append(tab)
            name = domain.player_rec.name
            self.tabs.addTab(tab, name)

    def refresh(self):
        for tab in self.player_tabs:
            tab.refresh()