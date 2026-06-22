from PyQt6.QtCore import (
    QAbstractTableModel,
    Qt,
    QModelIndex,
)
from db.models.item import Item


class ItemTableModel(QAbstractTableModel):
    HEADERS = ["ID", "Name", "Owner", "Container"]

    def __init__(self, items: list[Item] = []):
        super().__init__()
        self.items = items

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role):
        if (
            not index.isValid()
            or role != Qt.ItemDataRole.DisplayRole
        ):
            return None
        item = self.items[index.row()]
        col = index.column()
        return [
            item.id,
            item.name,
            item.owner_id,
            item.container_item_id,
        ][col]

    def headerData(self, section, orientation, role):
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return self.HEADERS[section]
        return None
