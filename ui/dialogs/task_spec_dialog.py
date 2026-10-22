# """
# TaskSpecDialog: builds a task.TaskSpec.

# Sections:
#   - Task preset picker (search by name/notes, "Create Task Preset..." button)
#   - Right side is disabled until a preset is selected -- this dialog only
#     makes sense as a way to build a TaskSpec on top of some preset.
#   - Selected preset: read-only display of the preset's own fields (task
#     kind is just the preset's name), shown for consultation only.
#   - Editable TaskSpec fields: workstation, duration override, workload
#     multiplier, repetition, output (mold + quantity range +
#     quality_dependent), participants/tools, risk profile, notes.

# "Create Task Preset..." just emits a signal for now -- the brief says that
# popup will be wired up later, so this dialog doesn't assume its shape.
# """

# from PyQt6.QtWidgets import (
#     QDialog,
#     QHBoxLayout,
#     QVBoxLayout,
#     QLabel,
#     QScrollArea,
#     QWidget,
#     QFormLayout,
#     QCheckBox,
#     QSpinBox,
#     QTableWidgetItem,
#     QDoubleSpinBox,
#     QTableWidget,
#     QPushButton,
#     QTabWidget,
#     QPlainTextEdit,
#     QDialogButtonBox,
#     QMessageBox,
# )
# from PyQt6.QtCore import Qt

# from systems.task_service.task import (
#     TaskSpec,
#     TaskOutput,
#     RiskEntry,
#     RepetitionSpec,
#     Technicality,
# )
# from systems.task_service.task_preset_repository import (
#     load_presets,
#     add_preset,
# )
# from ui.dialogs.task_preset_editor import (
#     CreateTaskPresetDialog,
# )
# from ui.widgets.searchable_preset_list import (
#     SearchablePresetList,
# )
# from ui.widgets.float_slider import FloatSlider
# from ui.widgets.searchable_record_picker import (
#     SearchableRecordPicker,
# )
# from ui.widgets.tool_assignment_widget import (
#     ToolAssignmentWidget,
# )


# def _mold_label(mold) -> str:
#     return mold.name


# class TaskSpecDialog(QDialog):
#     def __init__(
#         self,
#         item_repository,
#         participant_ids: list[int],
#         parent=None,
#     ):
#         """
#         item_repository: an ItemRepository (see item.py) used for the mold
#             and tool pickers.
#         participant_ids: participants performing this task. Solo tasks pass
#             a single id; cooperative tasks pass several and this dialog
#             builds one ToolAssignmentWidget per participant.
#         """
#         super().__init__(parent)
#         self.setWindowTitle("Create Task Spec")
#         self._item_repository = item_repository
#         self._selected_preset = None
#         self._spec_technicalities: dict[
#             str, Technicality
#         ] = {}

#         root = QHBoxLayout(self)

#         # --- Left column: preset picker -------------------------------
#         left = QVBoxLayout()
#         left.addWidget(QLabel("Task Preset"))
#         self.preset_list = SearchablePresetList(
#             load_presets()
#         )
#         self.preset_list.preset_selected.connect(
#             self._on_preset_selected
#         )
#         self.preset_list.create_requested.connect(
#             self._open_create_preset_dialog
#         )
#         left.addWidget(self.preset_list)
#         root.addLayout(left, stretch=1)

#         # --- Right column: everything else -----------------------------
#         right_scroll = QScrollArea()
#         right_scroll.setWidgetResizable(True)
#         self.right = QWidget()
#         self.right.setEnabled(
#             False
#         )  # gated on a preset being selected
#         form = QFormLayout(self.right)
#         right_scroll.setWidget(self.right)
#         root.addWidget(right_scroll, stretch=2)

#         # --- Selected preset: read-only, for consultation ---------------
#         form.addRow(QLabel("<b>Selected Preset</b>"))

#         self.task_kind_label = QLabel("—")
#         form.addRow("Task kind", self.task_kind_label)

#         self.preset_skill_track_label = QLabel("—")
#         form.addRow(
#             "Skill track", self.preset_skill_track_label
#         )

#         self.preset_components_label = QLabel("—")
#         self.preset_components_label.setWordWrap(True)
#         form.addRow(
#             "Task components", self.preset_components_label
#         )

#         self.preset_exp_effect_label = QLabel("—")
#         self.preset_exp_effect_label.setWordWrap(True)
#         form.addRow(
#             "Exp effect", self.preset_exp_effect_label
#         )

#         self.preset_base_workload_label = QLabel("—")
#         form.addRow(
#             "Base workload", self.preset_base_workload_label
#         )

#         self.preset_interruptibility_label = QLabel("—")
#         form.addRow(
#             "Interruptibility",
#             self.preset_interruptibility_label,
#         )

#         self.preset_min_lighting_label = QLabel("—")
#         form.addRow(
#             "Min lighting", self.preset_min_lighting_label
#         )

#         self.preset_notes_label = QLabel("—")
#         self.preset_notes_label.setWordWrap(True)
#         form.addRow("Preset notes", self.preset_notes_label)

#         # --- Editable TaskSpec fields ------------------------------------
#         form.addRow(QLabel("<b>Task Spec</b>"))

#         self.workstation_check = QCheckBox(
#             "Requires workstation"
#         )
#         self.workstation_spin = QSpinBox()
#         self.workstation_spin.setMaximum(1_000_000)
#         self.workstation_spin.setEnabled(False)
#         self.workstation_check.toggled.connect(
#             self.workstation_spin.setEnabled
#         )
#         workstation_row = QHBoxLayout()
#         workstation_row.addWidget(self.workstation_check)
#         workstation_row.addWidget(self.workstation_spin)
#         form.addRow("Workstation ID", workstation_row)

#         self.duration_override_check = QCheckBox(
#             "Override computed duration"
#         )
#         self.duration_override_spin = QSpinBox()
#         self.duration_override_spin.setMaximum(1_000_000)
#         self.duration_override_spin.setEnabled(False)
#         self.duration_override_check.toggled.connect(
#             self.duration_override_spin.setEnabled
#         )
#         duration_override_row = QHBoxLayout()
#         duration_override_row.addWidget(
#             self.duration_override_check
#         )
#         duration_override_row.addWidget(
#             self.duration_override_spin
#         )
#         form.addRow(
#             "Duration override (ticks)",
#             duration_override_row,
#         )

#         self.workload_slider = FloatSlider(
#             0.0, 3.0, step=0.05, value=1.0
#         )
#         form.addRow(
#             "Workload multiplier", self.workload_slider
#         )

#         # --- Technicalities: pre-filled from preset, remove-only ---------
#         form.addRow(QLabel("<b>Technicalities</b>"))
#         self.technicalities_table = QTableWidget(0, 4)
#         self.technicalities_table.setHorizontalHeaderLabels(
#             ["type", "explanation", "threshold", "weight"]
#         )
#         self.technicalities_table.setMaximumHeight(120)
#         form.addRow(self.technicalities_table)
#         technicality_buttons = QHBoxLayout()
#         remove_technicality_button = QPushButton(
#             "Remove Selected Technicality"
#         )
#         remove_technicality_button.clicked.connect(
#             self._remove_technicality_row
#         )
#         technicality_buttons.addWidget(
#             remove_technicality_button
#         )
#         form.addRow(technicality_buttons)

#         # --- Repetition ---------------------------------------------
#         self.rep_count_spin = QSpinBox()
#         self.rep_count_spin.setMaximum(1_000_000)
#         self.rep_target_spin = QSpinBox()
#         self.rep_target_spin.setMaximum(1_000_000)
#         self.rep_target_spin.setValue(1)
#         self.rep_strain_spin = QDoubleSpinBox()
#         self.rep_strain_spin.setRange(0.0, 100.0)
#         self.rep_strain_spin.setValue(1.0)
#         rep_row = QHBoxLayout()
#         rep_row.addWidget(QLabel("count"))
#         rep_row.addWidget(self.rep_count_spin)
#         rep_row.addWidget(QLabel("target"))
#         rep_row.addWidget(self.rep_target_spin)
#         rep_row.addWidget(QLabel("per-rep strain scalar"))
#         rep_row.addWidget(self.rep_strain_spin)
#         form.addRow("Repetition", rep_row)

#         # --- Output: mold + quantity range + quality_dependent --------
#         form.addRow(QLabel("<b>Output</b>"))

#         self.mold_picker = SearchableRecordPicker(
#             fetch_fn=lambda text: item_repository.get_all_molds(
#                 search=text
#             ),
#             label_fn=_mold_label,
#             placeholder="Search molds...",
#         )
#         form.addRow("Output mold", self.mold_picker)

#         self.quantity_min_spin = QSpinBox()
#         self.quantity_min_spin.setRange(0, 10_000)
#         self.quantity_min_spin.setValue(1)
#         self.quantity_max_spin = QSpinBox()
#         self.quantity_max_spin.setRange(0, 10_000)
#         self.quantity_max_spin.setValue(1)
#         quantity_row = QHBoxLayout()
#         quantity_row.addWidget(QLabel("min"))
#         quantity_row.addWidget(self.quantity_min_spin)
#         quantity_row.addWidget(QLabel("max"))
#         quantity_row.addWidget(self.quantity_max_spin)
#         form.addRow("Quantity range", quantity_row)

#         self.quality_dependent_check = QCheckBox(
#             "Yield grade depends on quality"
#         )
#         self.quality_dependent_check.setChecked(True)
#         form.addRow("", self.quality_dependent_check)

#         # --- Participants / equipped tools -----------------------------
#         form.addRow(QLabel("<b>Participants & Tools</b>"))
#         self._participant_widgets: list[
#             ToolAssignmentWidget
#         ] = []
#         participants_tabs = QTabWidget()
#         for participant_id in participant_ids:
#             widget = ToolAssignmentWidget(
#                 participant_id, item_repository
#             )
#             self._participant_widgets.append(widget)
#             participants_tabs.addTab(
#                 widget, f"Participant {participant_id}"
#             )
#         form.addRow(participants_tabs)

#         # --- Risk profile ------------------------------------------
#         form.addRow(QLabel("<b>Risk profile</b>"))
#         self.risk_table = QTableWidget(0, 4)
#         self.risk_table.setHorizontalHeaderLabels(
#             [
#                 "risk_type",
#                 "prob/tick",
#                 "severity min",
#                 "severity max",
#             ]
#         )
#         self.risk_table.setMaximumHeight(120)
#         form.addRow(self.risk_table)
#         risk_buttons = QHBoxLayout()
#         remove_risk_button = QPushButton(
#             "Remove Selected Risk"
#         )
#         remove_risk_button.clicked.connect(
#             self._remove_risk_row
#         )
#         risk_buttons.addWidget(remove_risk_button)
#         form.addRow(risk_buttons)

#         self.notes_edit = QPlainTextEdit()
#         self.notes_edit.setMaximumHeight(60)
#         form.addRow("Notes", self.notes_edit)

#         buttons = QDialogButtonBox(
#             QDialogButtonBox.StandardButton.Ok
#             | QDialogButtonBox.StandardButton.Cancel
#         )
#         buttons.accepted.connect(self._on_accept)
#         buttons.rejected.connect(self.reject)
#         form.addRow(buttons)

#     # --- Preset handling -------------------------------------------------

#     def _on_accept(self):
#         if self._selected_preset is None:
#             QMessageBox.warning(
#                 self,
#                 "Task preset required",
#                 "Select a task preset before creating a task spec.",
#             )
#             return
#         self.accept()

#     def _on_preset_selected(self, preset):
#         self._selected_preset = preset
#         self.right.setEnabled(True)

#         self.task_kind_label.setText(preset.name)
#         self.preset_skill_track_label.setText(
#             preset.skill_track.value
#         )

#         components_text = ", ".join(
#             f"{name}: {weight:g}"
#             for name, weight in preset.task_components.items()
#         )
#         self.preset_components_label.setText(
#             components_text or "—"
#         )

#         exp_axis_labels = [
#             "Intensity",
#             "Efficiency",
#             "Quality",
#             "Safety",
#         ]
#         exp_text = ", ".join(
#             f"{label}: {value:g}"
#             for label, value in zip(
#                 exp_axis_labels, preset.exp_effect
#             )
#         )
#         self.preset_exp_effect_label.setText(
#             exp_text or "—"
#         )

#         self.preset_base_workload_label.setText(
#             str(preset.metabolic_mult)
#         )
#         self.preset_interruptibility_label.setText(
#             preset.interruptibility.value
#         )
#         self.preset_min_lighting_label.setText(
#             str(preset.min_lighting)
#         )
#         self.preset_notes_label.setText(preset.notes or "—")

#         self._spec_technicalities = dict(
#             preset.technicalities
#         )
#         self._populate_technicalities_table(
#             self._spec_technicalities
#         )

#     def _open_create_preset_dialog(self):
#         preset = CreateTaskPresetDialog.get_task_preset()
#         if preset is not None:
#             updated = add_preset(preset)
#             self.preset_list.set_presets(updated)

#     # --- Technicalities table ------------------------------------------

#     def _populate_technicalities_table(
#         self, technicalities: dict[str, Technicality]
#     ):
#         self.technicalities_table.setRowCount(0)
#         for technicality in technicalities.values():
#             row = self.technicalities_table.rowCount()
#             self.technicalities_table.insertRow(row)
#             for col, text in enumerate(
#                 (
#                     technicality.type,
#                     technicality.explanation,
#                     f"{technicality.threshold:g}",
#                     f"{technicality.weight:g}",
#                 )
#             ):
#                 item = QTableWidgetItem(text)
#                 item.setFlags(
#                     item.flags()
#                     & ~Qt.ItemFlag.ItemIsEditable
#                 )
#                 self.technicalities_table.setItem(
#                     row, col, item
#                 )

#     def _remove_technicality_row(self):
#         for row in sorted(
#             {
#                 i.row()
#                 for i in self.technicalities_table.selectedIndexes()
#             },
#             reverse=True,
#         ):
#             type_item = self.technicalities_table.item(
#                 row, 0
#             )
#             if type_item is not None:
#                 self._spec_technicalities.pop(
#                     type_item.text(), None
#                 )
#             self.technicalities_table.removeRow(row)

#     # --- Risk table --------------------------------------------------

#     def _remove_risk_row(self):
#         for row in sorted(
#             {
#                 i.row()
#                 for i in self.risk_table.selectedIndexes()
#             },
#             reverse=True,
#         ):
#             self.risk_table.removeRow(row)

#     def _risk_profile(self) -> list[RiskEntry]:
#         entries = []
#         for row in range(self.risk_table.rowCount()):

#             def cell(col, default="0"):
#                 item = self.risk_table.item(row, col)
#                 return (
#                     item.text()
#                     if item and item.text()
#                     else default
#                 )

#             risk_type = cell(0, "")
#             if not risk_type:
#                 continue
#             entries.append(
#                 RiskEntry(
#                     risk_type=risk_type,
#                     base_probability_per_tick=float(
#                         cell(1)
#                     ),
#                     severity_range=(
#                         float(cell(2)),
#                         float(cell(3)),
#                     ),
#                 )
#             )
#         return entries

#     # --- Build result --------------------------------------------------

#     def build_task_spec(self) -> TaskSpec:
#         output = None
#         mold = self.mold_picker.selected()
#         if mold is not None:
#             output = TaskOutput(
#                 mold_id=mold.name,
#                 quantity_range=(
#                     self.quantity_min_spin.value(),
#                     self.quantity_max_spin.value(),
#                 ),
#                 quality_dependent=self.quality_dependent_check.isChecked(),
#             )

#         return TaskSpec(
#             task_preset=self._selected_preset.name,
#             total_workload=self.workload_slider.value(),
#             repetition=RepetitionSpec(
#                 rep_count=self.rep_count_spin.value(),
#                 rep_target=self.rep_target_spin.value(),
#                 per_rep_strain_scalar=self.rep_strain_spin.value(),
#             ),
#             output=output,
#             workstation_id=(
#                 self.workstation_spin.value()
#                 if self.workstation_check.isChecked()
#                 else None
#             ),
#             duration_override_ticks=(
#                 self.duration_override_spin.value()
#                 if self.duration_override_check.isChecked()
#                 else None
#             ),
#             technicalities=dict(self._spec_technicalities),
#             notes=self.notes_edit.toPlainText(),
#         )

#     @classmethod
#     def get_task_spec(
#         cls, item_repository, participant_ids, parent=None
#     ):
#         dialog = cls(
#             item_repository, participant_ids, parent
#         )
#         if dialog.exec():
#             return dialog.build_task_spec()
#         return None


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
  - Participants/tools: one ToolAssignmentWidget per participant. These are
    NOT part of TaskSpec (a spec is a reusable template); they are returned
    separately as ParticipantAssignments for whoever creates the
    TaskInstance. Use get_task_setup() to get both at once.
"""

from dataclasses import asdict

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

from core.defs.task import TaskOutput
from systems.task_service.task import (
    Technicality,
    ParticipantAssignment,
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

        self.preset_components_label = QLabel("—")
        self.preset_components_label.setWordWrap(True)
        form.addRow(
            "Task components", self.preset_components_label
        )

        self.preset_exp_effect_label = QLabel("—")
        self.preset_exp_effect_label.setWordWrap(True)
        form.addRow(
            "Exp effect", self.preset_exp_effect_label
        )

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
        self.technicalities_table = QTableWidget(0, 3)
        self.technicalities_table.setHorizontalHeaderLabels(
            ["key", "explanation", "trigger"]
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

        components_text = ", ".join(
            f"{name}: {weight:g}"
            for name, weight in preset.task_components.items()
        )
        self.preset_components_label.setText(
            components_text or "—"
        )

        exp_text = ", ".join(
            f"{label}: {value:g}"
            for label, value in zip(
                EXP_AXIS_LABELS, preset.exp_effect
            )
        )
        self.preset_exp_effect_label.setText(
            exp_text or "—"
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
            # JSON column: store plain dicts, not Technicality objects.
            technicalities={
                key: asdict(technicality)
                for key, technicality in self._spec_technicalities.items()
            },
            notes=self.notes_edit.toPlainText() or None,
        )

    def build_assignments(
        self,
    ) -> list[ParticipantAssignment]:
        return [
            widget.build_assignment()
            for widget in self._participant_widgets
        ]

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
        """Returns (TaskSpec, list[ParticipantAssignment]) or None."""
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
