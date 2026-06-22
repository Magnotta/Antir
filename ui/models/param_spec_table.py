from PyQt6.QtCore import (
    QAbstractTableModel,
    Qt,
    QModelIndex,
)
from db.models.item import ParamSpec


class ParamSpecTableModel(QAbstractTableModel):
    HEADERS = ["Param", "Base", "Variance"]

    def __init__(self, specs: list[ParamSpec], parent=None):
        super().__init__(parent)
        self.specs = specs

    def rowCount(self, parent=QModelIndex()):
        return len(self.specs)

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

        spec = self.specs[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            return [
                spec.param,
                spec.base,
                spec.variance,
            ][col]

        return None

    def add_spec(self, spec: ParamSpec):
        self.beginInsertRows(
            QModelIndex(), len(self.specs), len(self.specs)
        )
        self.specs.append(spec)
        self.endInsertRows()

    def remove_at(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.specs[row]
        self.endRemoveRows()
