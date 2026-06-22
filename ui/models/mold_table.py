from PyQt6.QtCore import (
    QAbstractTableModel,
    Qt,
    QModelIndex,
)
from db.models.item import Mold


class MoldTableModel(QAbstractTableModel):
    HEADERS = ["ID", "Name", "Tags", "Description"]

    def __init__(self, molds: list[Mold] = []):
        super().__init__()
        self.molds = molds

    def rowCount(self, parent=QModelIndex()):
        return len(self.molds)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if (
            not index.isValid()
            or role != Qt.ItemDataRole.DisplayRole
        ):
            return None
        item = self.molds[index.row()]
        col = index.column()
        return [
            item.id,
            item.name,
            item.tags,
            item.description,
        ][col]

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return section + 1

    def delete_row(self, row: int):
        item = self.molds[row]
        self.session.delete(item)
        self.session.commit()
        self.refresh()
