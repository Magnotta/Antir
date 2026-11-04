"""
ToolAssignmentWidget: one participant's equipment for a task.

A task preset has exactly one physical activity, so a participant has no
components to choose between -- just the tool(s) they bring to that one
activity:

    Tools for 'chopping'
    <list of currently-equipped tool items>
    [+ Add Tool]   [Remove Selected]

The widget doesn't know the preset by itself: the parent dialog calls
set_activity(preset.activity) whenever a preset is selected. "+ Add Tool"
then opens a RecordPickerDialog over ItemRepository.get_extant_items,
narrowed to items whose mold has a tool profile usable for that activity.
"""

from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QListWidget,
    QHBoxLayout,
    QPushButton,
    QListWidgetItem,
    QWidget,
)
from PyQt6.QtCore import Qt
from systems.item_service.classes import ToolName
from ui.dialogs.record_picker import (
    RecordPickerDialog,
)


def _item_label(item) -> str:
    return f"{item.name} (#{item.id})"


def _usable_for(item, activity: str) -> bool:
    """True if the item's mold is a tool that can be used for `activity`."""
    profile = item.mold.tool_name
    return profile in ToolName


class ToolAssignmentWidget(QWidget):
    """One of these per participant. `participant_id` is fixed at
    construction time (e.g. the acting character); the cooperative case
    just uses one of these per participant tab.

    max_tools: how many tools one participant may equip. Defaults to 1;
    the aspect calculation will take the best tool per aspect if you raise
    it later.
    """

    def __init__(
        self,
        participant_id: int,
        item_repository,
        parent=None,
        max_tools: int = 1,
    ):
        super().__init__(parent)
        self.participant_id = participant_id
        self._item_repository = item_repository
        self._max_tools = max_tools
        self._activity: str | None = None
        self._item_ids: list[int] = []

        layout = QVBoxLayout(self)

        self.header_label = QLabel()
        layout.addWidget(self.header_label)

        self.tool_list = QListWidget()
        self.tool_list.setMaximumHeight(90)
        layout.addWidget(self.tool_list)

        button_row = QHBoxLayout()
        self.add_button = QPushButton("+ Add Tool")
        self.add_button.clicked.connect(self._add_tool)
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(
            self._remove_selected
        )
        button_row.addWidget(self.add_button)
        button_row.addWidget(self.remove_button)
        layout.addLayout(button_row)

        self._update_ui()

    def set_activity(self, activity: str | None):
        """Call whenever the selected preset changes.

        Tool eligibility depends only on the activity, so tools are kept
        if two presets share one, and cleared if the activity changes.
        """
        if activity == self._activity:
            return
        self._activity = activity
        self._item_ids.clear()
        self.tool_list.clear()
        self._update_ui()

    def _update_ui(self):
        has_activity = self._activity is not None
        self.header_label.setText(
            f"Tools for '{self._activity}'"
            if has_activity
            else "Select a task preset to choose tools"
        )
        self.add_button.setEnabled(
            has_activity
            and len(self._item_ids) < self._max_tools
        )

    def _add_tool(self):
        activity = self._activity
        if activity is None:
            return
        item = RecordPickerDialog.get_record(
            fetch_fn=lambda text: [
                candidate
                for candidate in self._item_repository.get_extant_items(
                    search=text
                )
                if _usable_for(candidate, activity)
            ],
            label_fn=_item_label,
            title=f"Add tool for '{activity}'",
            placeholder="Search tools...",
            parent=self,
        )
        if item is None or item.id in self._item_ids:
            return
        self._item_ids.append(item.id)
        row = QListWidgetItem(_item_label(item))
        row.setData(Qt.ItemDataRole.UserRole, item.id)
        self.tool_list.addItem(row)
        self._update_ui()

    def _remove_selected(self):
        for row in self.tool_list.selectedItems():
            self._item_ids.remove(
                row.data(Qt.ItemDataRole.UserRole)
            )
            self.tool_list.takeItem(self.tool_list.row(row))
        self._update_ui()

    def equipped_tool_item_ids(self) -> list[int]:
        return list(self._item_ids)
