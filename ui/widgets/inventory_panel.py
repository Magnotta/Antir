from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QTableView,
    QVBoxLayout,
)


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
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return self.HEADERS[section]

    def data(self, index, role):
        if (
            not index.isValid()
            or role != Qt.ItemDataRole.DisplayRole
        ):
            return None
        item = self.items[index.row()]
        if item.destroyed:
            return None
        col = index.column()
        if col == 0:
            return item.id
        if col == 1:
            return (
                item.name
                if hasattr(item, "mold")
                else str(item.original_mold_id)
            )
        if col == 2:
            return self._location_text(item)
        if col == 3:
            return item.description

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
        items = self.inventory.get_items()
        self.model = InventoryTableModel(items)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()
