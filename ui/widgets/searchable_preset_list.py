"""
SearchablePresetList: search-as-you-type list of TaskPresets, plus a
'Create Task Preset...' button. Filtering happens in memory against the
already-loaded preset list (see task_preset_repository.search_presets), so
there's no debounce needed here -- unlike the DB-backed pickers for molds
and items.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
    QPushButton,
    QListWidgetItem,
)
from PyQt6.QtCore import Qt, pyqtSignal
from systems.task_service.task_preset_repository import (
    search_presets,
)


class SearchablePresetList(QWidget):
    # Emitted whenever the highlighted row changes, with the TaskPreset.
    preset_selected = pyqtSignal(object)
    # Emitted when "Create Task Preset..." is clicked. The parent dialog
    # owns what that actually opens (a second popup, per the brief).
    create_requested = pyqtSignal()

    def __init__(self, presets, parent=None):
        super().__init__(parent)
        self._all_presets = dict(presets)
        self._selected = None

        layout = QVBoxLayout(self)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
            "Search name or notes..."
        )
        self.search_box.textChanged.connect(self._refresh)
        layout.addWidget(self.search_box)

        self.list_widget = QListWidget()
        self.list_widget.currentItemChanged.connect(
            self._on_current_changed
        )
        layout.addWidget(self.list_widget)

        self.create_button = QPushButton(
            "Create Task Preset..."
        )
        self.create_button.clicked.connect(
            self.create_requested.emit
        )
        layout.addWidget(self.create_button)

        self._refresh()

    def set_presets(self, presets: dict):
        """Call after a new preset is created/saved elsewhere, to refresh
        the list without re-opening this widget."""
        self._all_presets = dict(presets.values())
        self._refresh()

    def selected_preset(self):
        return self._selected

    def _refresh(self):
        query = self.search_box.text()
        matches = search_presets(self._all_presets, query)

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for preset in matches:
            item = QListWidgetItem(preset.name)
            item.setData(Qt.ItemDataRole.UserRole, preset)
            if preset.notes:
                item.setToolTip(preset.notes)
            self.list_widget.addItem(item)
        self.list_widget.blockSignals(False)

        # Keep selection in sync with what's actually visible.
        if matches:
            self.list_widget.setCurrentRow(0)
        else:
            self._selected = None

    def _on_current_changed(self, current, _previous):
        self._selected = (
            current.data(Qt.ItemDataRole.UserRole)
            if current
            else None
        )
        if self._selected is not None:
            self.preset_selected.emit(self._selected)
