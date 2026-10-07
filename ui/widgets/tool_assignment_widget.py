"""
ToolAssignmentWidget: builds one participant's ParticipantAssignment --
the list of components they perform, and which item_ids are equipped as
tools for each component.

Layout per component ("chopping", "hauling", ...):
    [component name]                       [Remove Component]
    <list of currently-equipped tool items>
    [+ Add Tool]   [Remove Selected Tool]

"+ Add Tool" opens a RecordPickerDialog over ItemRepository.get_extant_items,
so the tool list always reflects items that actually exist and aren't
destroyed.
"""

from PyQt6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QListWidget,
    QHBoxLayout,
    QPushButton,
    QListWidgetItem,
    QWidget,
    QInputDialog,
)
from PyQt6.QtCore import Qt
from ui.dialogs.record_picker import (
    RecordPickerDialog,
)


def _item_label(item) -> str:
    return f"{item.name} (#{item.id})"


class ComponentToolRow(QGroupBox):
    def __init__(
        self,
        component_name: str,
        item_repository,
        parent=None,
    ):
        super().__init__(component_name, parent)
        self.component_name = component_name
        self._item_repository = item_repository
        self._item_ids: list[int] = []

        layout = QVBoxLayout(self)

        self.tool_list = QListWidget()
        self.tool_list.setMaximumHeight(90)
        layout.addWidget(self.tool_list)

        button_row = QHBoxLayout()
        add_button = QPushButton("+ Add Tool")
        add_button.clicked.connect(self._add_tool)
        remove_button = QPushButton("Remove Selected")
        remove_button.clicked.connect(self._remove_selected)
        button_row.addWidget(add_button)
        button_row.addWidget(remove_button)
        layout.addLayout(button_row)

    def _add_tool(self):
        item = RecordPickerDialog.get_record(
            fetch_fn=lambda text: self._item_repository.get_extant_items(
                search=text
            ),
            label_fn=_item_label,
            title=f"Add tool for '{self.component_name}'",
            placeholder="Search items...",
            parent=self,
        )
        if item is None or item.id in self._item_ids:
            return
        self._item_ids.append(item.id)
        row = QListWidgetItem(_item_label(item))
        row.setData(Qt.ItemDataRole.UserRole, item.id)
        self.tool_list.addItem(row)

    def _remove_selected(self):
        for row in self.tool_list.selectedItems():
            self._item_ids.remove(
                row.data(Qt.ItemDataRole.UserRole)
            )
            self.tool_list.takeItem(self.tool_list.row(row))

    def item_ids(self) -> list[int]:
        return list(self._item_ids)


class ToolAssignmentWidget(QWidget):
    """One of these per participant. `participant_id` is fixed at
    construction time (e.g. the acting character); the brief's multi-
    participant cooperative case can reuse one of these per participant tab.
    """

    def __init__(
        self,
        participant_id: int,
        item_repository,
        parent=None,
    ):
        super().__init__(parent)
        self.participant_id = participant_id
        self._item_repository = item_repository
        self._rows: dict[str, ComponentToolRow] = {}

        layout = QVBoxLayout(self)

        self.rows_layout = QVBoxLayout()
        layout.addLayout(self.rows_layout)

        add_component_button = QPushButton(
            "+ Add Component"
        )
        add_component_button.clicked.connect(
            self._add_component
        )
        layout.addWidget(add_component_button)

    def _add_component(self):
        name, ok = QInputDialog.getText(
            self,
            "Add Component",
            "Activity/component name:",
        )
        name = name.strip()
        if not ok or not name or name in self._rows:
            return
        row = ComponentToolRow(name, self._item_repository)
        self._rows[name] = row
        self.rows_layout.addWidget(row)

    def components(self) -> list[str]:
        return list(self._rows.keys())

    def equipped_tool_item_ids(
        self,
    ) -> dict[str, list[int]]:
        return {
            name: row.item_ids()
            for name, row in self._rows.items()
        }
