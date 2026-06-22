from PyQt6.QtCore import (
    QAbstractTableModel,
    Qt,
    QModelIndex,
)
from db.models.item import ItemParam


class ItemParamTableModel(QAbstractTableModel):
    HEADERS = ["Param", "Value"]

    def __init__(
        self, params: list[ItemParam], parent=None
    ):
        super().__init__(parent)
        self.params = params

    def rowCount(self, parent=QModelIndex()):
        return len(self.params)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return section + 1

    def data(self, index, role):
        if not index.isValid():
            return None

        param = self.params[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            return [
                param.name,
                param.value,
            ][col]
