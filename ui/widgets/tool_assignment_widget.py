<<<<<<< HEAD
# """
# ToolAssignmentWidget: builds one participant's ParticipantAssignment --
# the list of components they perform, and which item_ids are equipped as
# tools for each component.

# Layout per component ("chopping", "hauling", ...):
#     [component name]                       [Remove Component]
#     <list of currently-equipped tool items>
#     [+ Add Tool]   [Remove Selected Tool]

# "+ Add Tool" opens a RecordPickerDialog over ItemRepository.get_extant_items,
# so the tool list always reflects items that actually exist and aren't
# destroyed.
# """

# from PyQt6.QtWidgets import (
#     QGroupBox,
#     QVBoxLayout,
#     QListWidget,
#     QHBoxLayout,
#     QPushButton,
#     QListWidgetItem,
#     QWidget,
#     QInputDialog,
# )
# from PyQt6.QtCore import Qt
# from ui.dialogs.record_picker import (
#     RecordPickerDialog,
# )


# def _item_label(item) -> str:
#     return f"{item.name} (#{item.id})"


# class ComponentToolRow(QGroupBox):
#     def __init__(
#         self,
#         component_name: str,
#         item_repository,
#         parent=None,
#     ):
#         super().__init__(component_name, parent)
#         self.component_name = component_name
#         self._item_repository = item_repository
#         self._item_ids: list[int] = []

#         layout = QVBoxLayout(self)

#         self.tool_list = QListWidget()
#         self.tool_list.setMaximumHeight(90)
#         layout.addWidget(self.tool_list)

#         button_row = QHBoxLayout()
#         add_button = QPushButton("+ Add Tool")
#         add_button.clicked.connect(self._add_tool)
#         remove_button = QPushButton("Remove Selected")
#         remove_button.clicked.connect(self._remove_selected)
#         button_row.addWidget(add_button)
#         button_row.addWidget(remove_button)
#         layout.addLayout(button_row)

#     def _add_tool(self):
#         item = RecordPickerDialog.get_record(
#             fetch_fn=lambda text: self._item_repository.get_extant_items(
#                 search=text
#             ),
#             label_fn=_item_label,
#             title=f"Add tool for '{self.component_name}'",
#             placeholder="Search items...",
#             parent=self,
#         )
#         if item is None or item.id in self._item_ids:
#             return
#         self._item_ids.append(item.id)
#         row = QListWidgetItem(_item_label(item))
#         row.setData(Qt.ItemDataRole.UserRole, item.id)
#         self.tool_list.addItem(row)

#     def _remove_selected(self):
#         for row in self.tool_list.selectedItems():
#             self._item_ids.remove(
#                 row.data(Qt.ItemDataRole.UserRole)
#             )
#             self.tool_list.takeItem(self.tool_list.row(row))

#     def item_ids(self) -> list[int]:
#         return list(self._item_ids)


# class ToolAssignmentWidget(QWidget):
#     """One of these per participant. `participant_id` is fixed at
#     construction time (e.g. the acting character); the brief's multi-
#     participant cooperative case can reuse one of these per participant tab.
#     """

#     def __init__(
#         self,
#         participant_id: int,
#         item_repository,
#         parent=None,
#     ):
#         super().__init__(parent)
#         self.participant_id = participant_id
#         self._item_repository = item_repository
#         self._rows: dict[str, ComponentToolRow] = {}

#         layout = QVBoxLayout(self)

#         self.rows_layout = QVBoxLayout()
#         layout.addLayout(self.rows_layout)

#         add_component_button = QPushButton(
#             "+ Add Component"
#         )
#         add_component_button.clicked.connect(
#             self._add_component
#         )
#         layout.addWidget(add_component_button)

#     def _add_component(self):
#         name, ok = QInputDialog.getText(
#             self,
#             "Add Component",
#             "Activity/component name:",
#         )
#         name = name.strip()
#         if not ok or not name or name in self._rows:
#             return
#         row = ComponentToolRow(name, self._item_repository)
#         self._rows[name] = row
#         self.rows_layout.addWidget(row)

#     def components(self) -> list[str]:
#         return list(self._rows.keys())

#     def equipped_tool_item_ids(
#         self,
#     ) -> dict[str, list[int]]:
#         return {
#             name: row.item_ids()
#             for name, row in self._rows.items()
#         }


"""
ToolAssignmentWidget: builds one participant's ParticipantAssignment --
the list of components (physical activities) they perform, and which
item_ids are equipped as tools for each component. See build_assignment().

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
=======
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
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
    QVBoxLayout,
    QListWidget,
    QHBoxLayout,
    QPushButton,
    QListWidgetItem,
    QWidget,
<<<<<<< HEAD
    QInputDialog,
)
from PyQt6.QtCore import Qt
from systems.task_service.task import ParticipantAssignment
from systems.task_service.physical_activities import (
    PHYSICAL_ACTIVITIES_DICT,
)
=======
)
from PyQt6.QtCore import Qt
from systems.item_service.classes import ToolName
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
from ui.dialogs.record_picker import (
    RecordPickerDialog,
)


def _item_label(item) -> str:
    return f"{item.name} (#{item.id})"


<<<<<<< HEAD
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
=======
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
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
        self._item_ids: list[int] = []

        layout = QVBoxLayout(self)

<<<<<<< HEAD
=======
        self.header_label = QLabel()
        layout.addWidget(self.header_label)

>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
        self.tool_list = QListWidget()
        self.tool_list.setMaximumHeight(90)
        layout.addWidget(self.tool_list)

        button_row = QHBoxLayout()
<<<<<<< HEAD
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
=======
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
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
            parent=self,
        )
        if item is None or item.id in self._item_ids:
            return
        self._item_ids.append(item.id)
        row = QListWidgetItem(_item_label(item))
        row.setData(Qt.ItemDataRole.UserRole, item.id)
        self.tool_list.addItem(row)
<<<<<<< HEAD
=======
        self._update_ui()
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)

    def _remove_selected(self):
        for row in self.tool_list.selectedItems():
            self._item_ids.remove(
                row.data(Qt.ItemDataRole.UserRole)
            )
            self.tool_list.takeItem(self.tool_list.row(row))
<<<<<<< HEAD

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
        # Components are physical activities, so pick from the known ones
        # instead of typing a free-form name.
        available = [
            name
            for name in PHYSICAL_ACTIVITIES_DICT
            if name not in self._rows
        ]
        if not available:
            return
        name, ok = QInputDialog.getItem(
            self,
            "Add Component",
            "Physical activity:",
            available,
            0,
            False,
        )
        if not ok or not name:
            return
        row = ComponentToolRow(name, self._item_repository)
        self._rows[name] = row
        self.rows_layout.addWidget(row)

    def components(self) -> list[str]:
        return list(self._rows.keys())

    def build_assignment(self) -> ParticipantAssignment:
        return ParticipantAssignment(
            participant_id=self.participant_id,
            components=self.components(),
            equipped_tool_item_ids=self.equipped_tool_item_ids(),
        )

    def equipped_tool_item_ids(
        self,
    ) -> dict[str, list[int]]:
        return {
            name: row.item_ids()
            for name, row in self._rows.items()
        }
=======
        self._update_ui()

    def equipped_tool_item_ids(self) -> list[int]:
        return list(self._item_ids)
>>>>>>> 0f59876 (Added foundation for task execution. Reorganized systems into classes files)
