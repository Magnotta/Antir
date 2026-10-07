"""
SearchableRecordPicker: generic 'type to filter, pick one row' widget for
DB-backed records. It doesn't know anything about Molds or Items -- you hand
it a fetch function and a label function, so it works for either (or
anything else queried through a repository).

Debounced so it doesn't hit the DB on every keystroke.
"""

from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
)


class SearchableRecordPicker(QWidget):
    record_selected = pyqtSignal(object)

    def __init__(
        self,
        fetch_fn,
        label_fn,
        placeholder: str = "Search...",
        debounce_ms: int = 200,
        max_list_height: int = 140,
        parent=None,
    ):
        """
        fetch_fn: callable(search_text: str | None) -> list[record]
                  e.g. lambda text: item_repo.get_all_molds(search=text)
        label_fn: callable(record) -> str, used as the list row text.
        """
        super().__init__(parent)
        self._fetch_fn = fetch_fn
        self._label_fn = label_fn
        self._selected = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(placeholder)
        layout.addWidget(self.search_box)

        self.list_widget = QListWidget()
        self.list_widget.setMaximumHeight(max_list_height)
        self.list_widget.currentItemChanged.connect(
            self._on_current_changed
        )
        layout.addWidget(self.list_widget)

        self._debounce = QTimer(self)
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(debounce_ms)
        self._debounce.timeout.connect(self._run_search)
        self.search_box.textChanged.connect(
            lambda _text: self._debounce.start()
        )

        self._run_search()

    def _run_search(self):
        text = self.search_box.text().strip() or None
        results = self._fetch_fn(text)
        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for record in results:
            item = QListWidgetItem(self._label_fn(record))
            item.setData(Qt.ItemDataRole.UserRole, record)
            self.list_widget.addItem(item)
        self.list_widget.blockSignals(False)

    def _on_current_changed(self, current, _previous):
        self._selected = (
            current.data(Qt.ItemDataRole.UserRole)
            if current
            else None
        )
        if self._selected is not None:
            self.record_selected.emit(self._selected)

    def selected(self):
        return self._selected

    def refresh(self):
        self._run_search()
