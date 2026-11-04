"""
TaskSpecDialog: builds a task.TaskSpec (and the per-participant tool
assignments that go with it).

Sections:
  - Task preset picker (search by name, "Create Task Preset..." button)
  - Right side is disabled until a preset is selected -- this dialog only
    makes sense as a way to build a TaskSpec on top of some preset.
  - Selected preset: read-only display of the preset's own fields (task
    kind is just the preset's name), shown for consultation only.
  - Editable TaskSpec fields: total workload, cooperation profile,
    workstation, duration override, technicalities (remove-only, pre-filled
    from the preset), output (mold + quantity + quality mapping), notes.
  - Participants/tools: one ToolAssignmentWidget per participant. A preset
    has a single physical activity, so each widget is just a tool list for
    that activity; selecting a preset tells every widget which activity to
    filter tools by. These are NOT part of TaskSpec (a spec is a reusable
    template); build_assignments() returns them separately for whoever
    creates the TaskInstance. Use get_task_setup() to get both at once.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QWidget,
    QFormLayout,
    QCheckBox,
    QSpinBox,
    QTableWidgetItem,
    QTableWidget,
    QPushButton,
    QTabWidget,
    QPlainTextEdit,
    QDialogButtonBox,
    QMessageBox,
    QComboBox,
    QLineEdit,
    QHeaderView,
)
from PyQt6.QtCore import Qt

from systems.task_service.classes import (
    TaskOutput,
    Technicality,
)
from systems.task_service.task_preset_repository import (
    load_presets,
    add_preset,
)
from db.models.task import TaskSpec
from ui.dialogs.task_preset_editor import (
    CreateTaskPresetDialog,
)
from ui.widgets.searchable_preset_list import (
    SearchablePresetList,
)
from ui.widgets.searchable_record_picker import (
    SearchableRecordPicker,
)
from ui.widgets.tool_assignment_widget import (
    ToolAssignmentWidget,
)

EXP_AXIS_LABELS = [
    "Intensity",
    "Efficiency",
    "Quality",
    "Safety",
]


def _mold_label(mold) -> str:
    return mold.name


class TaskSpecDialog(QDialog):
    def __init__(
        self,
        item_repository,
        participant_ids: list[int],
        parent=None,
        cooperation_profiles: dict | None = None,
    ):
        """
        item_repository: an ItemRepository (see item.py) used for the mold
            and tool pickers.
        participant_ids: participants performing this task. Solo tasks pass
            a single id; cooperative tasks pass several and this dialog
            builds one ToolAssignmentWidget per participant.
        cooperation_profiles: optional {key: CooperationProfile} used to
            fill the cooperation profile dropdown. TaskSpec only stores the
            key. With none given, the only choice is "(none)".
        """
        super().__init__(parent)
        self.setWindowTitle("Create Task Spec")
        self._item_repository = item_repository
        self._selected_preset = None
        self._spec_technicalities: dict[
            str, Technicality
        ] = {}

        root = QHBoxLayout(self)

        # --- Left column: preset picker -------------------------------
        left = QVBoxLayout()
        left.addWidget(QLabel("Task Preset"))
        self.preset_list = SearchablePresetList(
            load_presets()
        )
        self.preset_list.preset_selected.connect(
            self._on_preset_selected
        )
        self.preset_list.create_requested.connect(
            self._open_create_preset_dialog
        )
        left.addWidget(self.preset_list)
        root.addLayout(left, stretch=1)

        # --- Right column: everything else -----------------------------
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        self.right = QWidget()
        self.right.setEnabled(
            False
        )  # gated on a preset being selected
        form = QFormLayout(self.right)
        right_scroll.setWidget(self.right)
        root.addWidget(right_scroll, stretch=2)

        # --- Selected preset: read-only, for consultation ---------------
        form.addRow(QLabel("<b>Selected Preset</b>"))

        self.task_kind_label = QLabel("—")
        form.addRow("Task kind", self.task_kind_label)

        self.preset_skill_track_label = QLabel("—")
        form.addRow(
            "Skill track", self.preset_skill_track_label
        )

        self.preset_activity_label = QLabel("—")
        form.addRow(
            "Physical activity", self.preset_activity_label
        )

        self.preset_tool_label = QLabel("—")
        form.addRow("Tool mode", self.preset_tool_label)

        self.preset_metabolic_mult_label = QLabel("—")
        form.addRow(
            "Metabolic multiplier",
            self.preset_metabolic_mult_label,
        )

        self.preset_interruptibility_label = QLabel("—")
        form.addRow(
            "Interruptibility",
            self.preset_interruptibility_label,
        )

        self.preset_min_lighting_label = QLabel("—")
        form.addRow(
            "Min lighting", self.preset_min_lighting_label
        )

        # --- Editable TaskSpec fields ------------------------------------
        form.addRow(QLabel("<b>Task Spec</b>"))

        self.total_workload_spin = QSpinBox()
        self.total_workload_spin.setRange(1, 1_000_000)
        self.total_workload_spin.setValue(100)
        form.addRow(
            "Total workload", self.total_workload_spin
        )

        self.cooperation_combo = QComboBox()
        self.cooperation_combo.addItem("(none)", None)
        for key in cooperation_profiles or {}:
            self.cooperation_combo.addItem(key, key)
        form.addRow(
            "Cooperation profile", self.cooperation_combo
        )

        self.workstation_check = QCheckBox(
            "Requires workstation"
        )
        self.workstation_spin = QSpinBox()
        self.workstation_spin.setMaximum(1_000_000)
        self.workstation_spin.setEnabled(False)
        self.workstation_check.toggled.connect(
            self.workstation_spin.setEnabled
        )
        workstation_row = QHBoxLayout()
        workstation_row.addWidget(self.workstation_check)
        workstation_row.addWidget(self.workstation_spin)
        form.addRow("Workstation ID", workstation_row)

        self.duration_override_check = QCheckBox(
            "Override computed duration"
        )
        self.duration_override_spin = QSpinBox()
        self.duration_override_spin.setMaximum(1_000_000)
        self.duration_override_spin.setEnabled(False)
        self.duration_override_check.toggled.connect(
            self.duration_override_spin.setEnabled
        )
        duration_override_row = QHBoxLayout()
        duration_override_row.addWidget(
            self.duration_override_check
        )
        duration_override_row.addWidget(
            self.duration_override_spin
        )
        form.addRow(
            "Duration override (ticks)",
            duration_override_row,
        )

        # --- Technicalities: pre-filled from preset, remove-only ---------
        form.addRow(QLabel("<b>Technicalities</b>"))
        self.technicalities_table = QTableWidget(0, 5)
        self.technicalities_table.setHorizontalHeaderLabels(
            [
                "key",
                "explanation",
                "trigger",
                "policy",
                "at",
            ]
        )
        self.technicalities_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.technicalities_table.setMaximumHeight(120)
        form.addRow(self.technicalities_table)
        technicality_buttons = QHBoxLayout()
        remove_technicality_button = QPushButton(
            "Remove Selected Technicality"
        )
        remove_technicality_button.clicked.connect(
            self._remove_technicality_row
        )
        technicality_buttons.addWidget(
            remove_technicality_button
        )
        form.addRow(technicality_buttons)

        # --- Output: mold + quantity + quality mapping -----------------
        form.addRow(QLabel("<b>Output</b>"))

        self.mold_picker = SearchableRecordPicker(
            fetch_fn=lambda text: item_repository.get_all_molds(
                search=text
            ),
            label_fn=_mold_label,
            placeholder="Search molds...",
        )
        form.addRow("Output mold", self.mold_picker)

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(0, 10_000)
        self.quantity_spin.setValue(1)
        form.addRow("Quantity", self.quantity_spin)

        self.quality_mapping_edit = QLineEdit()
        self.quality_mapping_edit.setPlaceholderText(
            "quality mapping key"
        )
        form.addRow(
            "Quality mapping", self.quality_mapping_edit
        )

        # --- Participants / equipped tools -----------------------------
        form.addRow(QLabel("<b>Participants & Tools</b>"))
        self._participant_widgets: list[
            ToolAssignmentWidget
        ] = []
        participants_tabs = QTabWidget()
        for participant_id in participant_ids:
            widget = ToolAssignmentWidget(
                participant_id, item_repository
            )
            self._participant_widgets.append(widget)
            participants_tabs.addTab(
                widget, f"Participant {participant_id}"
            )
        form.addRow(participants_tabs)

        self.notes_edit = QPlainTextEdit()
        self.notes_edit.setMaximumHeight(60)
        form.addRow("Notes", self.notes_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

        # SearchablePresetList highlights its first row while it is being
        # built, before we connected to its signal, so that selection never
        # reached us. Sync with it now that everything exists.
        initial = self.preset_list.selected_preset()
        if initial is not None:
            self._on_preset_selected(initial)

    # --- Preset handling -------------------------------------------------

    def _on_accept(self):
        if self._selected_preset is None:
            QMessageBox.warning(
                self,
                "Task preset required",
                "Select a task preset before creating a task spec.",
            )
            return
        self.accept()

    def _on_preset_selected(self, preset):
        self._selected_preset = preset
        self.right.setEnabled(True)

        self.task_kind_label.setText(preset.name)
        self.preset_skill_track_label.setText(
            preset.skill_track.value
        )

        self.preset_activity_label.setText(preset.activity)

        self.preset_tool_label.setText(
            preset.tool_mode.value
        )

        self.preset_metabolic_mult_label.setText(
            f"{preset.metabolic_mult:g}"
        )
        self.preset_interruptibility_label.setText(
            preset.interruptibility.value
        )
        self.preset_min_lighting_label.setText(
            str(preset.min_lighting)
        )

        self._spec_technicalities = dict(
            preset.technicalities
        )
        self._populate_technicalities_table(
            self._spec_technicalities
        )

        # Tool eligibility depends on the preset's activity; widgets clear
        # their tools only if the activity actually changed.
        for widget in self._participant_widgets:
            widget.set_activity(preset.activity)

    def _open_create_preset_dialog(self):
        preset = CreateTaskPresetDialog.get_task_preset(
            self
        )
        if preset is not None:
            updated = add_preset(preset)
            self.preset_list.set_presets(updated)

    # --- Technicalities table ------------------------------------------

    def _populate_technicalities_table(
        self, technicalities: dict[str, Technicality]
    ):
        self.technicalities_table.setRowCount(0)
        for technicality in technicalities.values():
            row = self.technicalities_table.rowCount()
            self.technicalities_table.insertRow(row)
            for col, text in enumerate(
                (
                    technicality.key,
                    technicality.explanation,
                    technicality.trigger_handle,
                    technicality.trigger_policy.value,
                    (
                        f"{technicality.trigger_time:g}"
                        if technicality.trigger_policy.value
                        == "once"
                        else "—"
                    ),
                )
            ):
                item = QTableWidgetItem(text)
                item.setFlags(
                    item.flags()
                    & ~Qt.ItemFlag.ItemIsEditable
                )
                self.technicalities_table.setItem(
                    row, col, item
                )

    def _remove_technicality_row(self):
        for row in sorted(
            {
                i.row()
                for i in self.technicalities_table.selectedIndexes()
            },
            reverse=True,
        ):
            key_item = self.technicalities_table.item(
                row, 0
            )
            if key_item is not None:
                self._spec_technicalities.pop(
                    key_item.text(), None
                )
            self.technicalities_table.removeRow(row)

    # --- Build results -------------------------------------------------

    def build_task_spec(self) -> TaskSpec:
        output = None
        mold = self.mold_picker.selected()
        if mold is not None:
            output = TaskOutput(
                mold_id=mold.id,
                quality_mapping=self.quality_mapping_edit.text().strip(),
                quantity=self.quantity_spin.value(),
            ).to_json()
        if self._selected_preset is None:
            raise (ValueError("No preset selected!"))

        return TaskSpec(
            task_preset=self._selected_preset.name,
            total_workload=self.total_workload_spin.value(),
            cooperation_profile=self.cooperation_combo.currentData(),
            output=output,
            workstation_id=(
                self.workstation_spin.value()
                if self.workstation_check.isChecked()
                else None
            ),
            duration_override_ticks=(
                self.duration_override_spin.value()
                if self.duration_override_check.isChecked()
                else None
            ),
            technicalities={
                key: technicality.to_json()
                for key, technicality in self._spec_technicalities.items()
            },
            notes=self.notes_edit.toPlainText() or None,
        )

    def build_assignments(self) -> dict[int, list[int]]:
        """participant_id -> equipped tool item ids.

        Stopgap: swap for ParticipantAssignment objects once that class is
        redefined for the single-activity model.
        """
        return {
            widget.participant_id: widget.equipped_tool_item_ids()
            for widget in self._participant_widgets
        }

    @classmethod
    def get_task_spec(
        cls,
        item_repository,
        participant_ids,
        parent=None,
        cooperation_profiles=None,
    ):
        dialog = cls(
            item_repository,
            participant_ids,
            parent,
            cooperation_profiles,
        )
        if dialog.exec():
            return dialog.build_task_spec()
        return None

    @classmethod
    def get_task_setup(
        cls,
        item_repository,
        participant_ids,
        parent=None,
        cooperation_profiles=None,
    ):
        """Returns (TaskSpec, {participant_id: [tool item ids]}) or None."""
        dialog = cls(
            item_repository,
            participant_ids,
            parent,
            cooperation_profiles,
        )
        if dialog.exec():
            return (
                dialog.build_task_spec(),
                dialog.build_assignments(),
            )
        return None
