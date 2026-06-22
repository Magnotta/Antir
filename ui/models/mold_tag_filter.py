from PyQt6.QtCore import (
    Qt,
    QSortFilterProxyModel,
)


class TagFilterModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )

    def set_filter_text(self, text: str):
        self.setFilterFixedString(text)

    def filterAcceptsRow(self, row, parent):
        if not self.filterRegularExpression().pattern():
            return True
        source = self.sourceModel().index(row, 0, parent)
        return (
            self.filterRegularExpression().pattern().lower()
            in source.data().lower()
        )
