"""
CreateTaskPresetDialog: builds a TaskPreset.

Mirrors TaskSpecDialog's pattern: build_task_preset() constructs the
dataclass from the widgets, get_task_preset() runs the dialog modally and
returns the built preset (or None if cancelled). This dialog doesn't save
anything itself -- same division of labor as TaskSpecDialog not saving the
TaskSpec it builds. Wiring it into the "Create Task Preset..." button looks
like:

    preset = CreateTaskPresetDialog.get_task_preset(self)
    if preset is not None:
        updated = add_preset(preset)
        self.preset_list.set_presets(updated)
"""

from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QTableWidget,
    QComboBox,
    QHBoxLayout,
    QPlainTextEdit,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QDialogButtonBox,
    QTableWidgetItem,
    QMessageBox,
    QAbstractItemView,
    QHeaderView,
)
from systems.task_service.classes import (
    SkillTrack,
    Interruptibility,
    Technicality,
    TaskPreset,
    TriggerPolicy,
)
from systems.item_service.classes import ToolModality
from systems.task_service.physical_activities import (
    PHYSICAL_ACTIVITIES_DICT,
)

EXP_COEFFS_LABELS = [
    "Intensity",
    "Efficiency",
    "Quality",
    "Safety",
]

# The only TriggerPolicy member whose trigger_time matters.
_ONCE = TriggerPolicy.ONCE


class TechnicalityFormDialog(QDialog):
    """Small popup form for creating or editing a single Technicality.

    A Technicality is (key, explanation, trigger_handle, trigger_policy,
    trigger_time). The handle is the name under which the trigger function
    is registered (see technicalities.py); the function itself isn't built
    here. trigger_time is an int: the percent (0-100) of task progress at
    which a "once" trigger is checked. It only applies to that policy, so
    the field is disabled for the others.
    """

    def __init__(
        self,
        parent=None,
        existing: Technicality | None = None,
    ):
        super().__init__(parent)
        self.setWindowTitle(
            "Edit Technicality"
            if existing
            else "New Technicality"
        )

        form = QFormLayout(self)

        self.key_edit = QLineEdit()
        form.addRow("Key", self.key_edit)

        self.explanation_edit = QPlainTextEdit()
        self.explanation_edit.setMaximumHeight(60)
        form.addRow("Explanation", self.explanation_edit)

        self.trigger_edit = QLineEdit()
        self.trigger_edit.setPlaceholderText(
            "registered trigger function name"
        )
        form.addRow("Trigger handle", self.trigger_edit)

        self.trigger_policy_combo = QComboBox()
        for option in TriggerPolicy:
            self.trigger_policy_combo.addItem(
                option.value, option.value
            )
        form.addRow(
            "Trigger policy", self.trigger_policy_combo
        )

        self.trigger_time_spin = QSpinBox()
        self.trigger_time_spin.setRange(0, 100)
        self.trigger_time_spin.setSingleStep(5)
        self.trigger_time_spin.setSuffix(" %")
        self.trigger_time_spin.setValue(100)
        self.trigger_time_spin.setToolTip(
            "Percent of task progress at which a 'once' trigger is "
            "checked (100 = on completion)."
        )
        form.addRow(
            "Trigger at (progress)", self.trigger_time_spin
        )

        self.trigger_policy_combo.currentIndexChanged.connect(
            self._sync_trigger_time_enabled
        )

        if existing is not None:
            self.key_edit.setText(existing.key)
            self.explanation_edit.setPlainText(
                existing.explanation
            )
            self.trigger_edit.setText(
                existing.trigger_handle
            )
            self.trigger_policy_combo.setCurrentIndex(
                self.trigger_policy_combo.findData(
                    existing.trigger_policy.value
                )
            )
            self.trigger_time_spin.setValue(
                existing.trigger_time
            )
        self._sync_trigger_time_enabled()

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _selected_policy(self) -> TriggerPolicy:
        return TriggerPolicy(
            self.trigger_policy_combo.currentData()
        )

    def _sync_trigger_time_enabled(self):
        self.trigger_time_spin.setEnabled(
            self._selected_policy() is _ONCE
        )

    def _on_accept(self):
        if not self.key_edit.text().strip():
            QMessageBox.warning(
                self,
                "Key required",
                "Give the technicality a key.",
            )
            return
        if not self.trigger_edit.text().strip():
            QMessageBox.warning(
                self,
                "Trigger handle required",
                "A technicality without a trigger can never fire.",
            )
            return
        self.accept()

    def build_technicality(self) -> Technicality:
        return Technicality(
            key=self.key_edit.text().strip(),
            explanation=self.explanation_edit.toPlainText(),
            trigger_handle=self.trigger_edit.text().strip(),
            trigger_policy=self._selected_policy(),
            trigger_time=self.trigger_time_spin.value(),
        )

    @classmethod
    def get_technicality(cls, parent=None, existing=None):
        dialog = cls(parent, existing=existing)
        if dialog.exec():
            return dialog.build_technicality()
        return None


class CreateTaskPresetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Task Preset")

        form = QFormLayout(self)

        self.name_edit = QLineEdit()
        form.addRow("Name", self.name_edit)

        self.skill_track_combo = QComboBox()
        for option in SkillTrack:
            self.skill_track_combo.addItem(
                option.value, option
            )
        form.addRow("Skill track", self.skill_track_combo)

        # --- activity: one physical activity per preset -----------------
        # TaskPreset.activity is a PhysicalActivityName, not free text, so
        # remember each dict key itself and hand that back from
        # build_task_preset() instead of the combo's display string.
        self.activity_combo = QComboBox()
        self._activities = {}
        for activity in PHYSICAL_ACTIVITIES_DICT.keys():
            label = str(
                getattr(activity, "value", activity)
            )
            self._activities[label] = activity
            self.activity_combo.addItem(label)
        form.addRow(
            "Physical activity", self.activity_combo
        )

        self.tool_mode_combo = QComboBox()
        for option in ToolModality:
            self.tool_mode_combo.addItem(
                option.value, option
            )
        form.addRow("Tool mode", self.tool_mode_combo)

        # --- technicalities: dict[str, Technicality] ----------------------
        self.technicalities: dict[str, Technicality] = {}
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
        self.technicalities_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.technicalities_table.cellDoubleClicked.connect(
            self._edit_technicality_row
        )
        form.addRow(
            "Technicalities", self.technicalities_table
        )

        technicality_buttons = QHBoxLayout()
        add_technicality_button = QPushButton(
            "New Technicality"
        )
        add_technicality_button.clicked.connect(
            self._add_technicality
        )
        remove_technicality_button = QPushButton(
            "Remove Selected"
        )
        remove_technicality_button.clicked.connect(
            self._remove_technicality_row
        )
        technicality_buttons.addWidget(
            add_technicality_button
        )
        technicality_buttons.addWidget(
            remove_technicality_button
        )
        form.addRow("", technicality_buttons)

        self.metabolic_mult_spin = QDoubleSpinBox()
        self.metabolic_mult_spin.setRange(0.0, 100.0)
        self.metabolic_mult_spin.setDecimals(2)
        self.metabolic_mult_spin.setSingleStep(0.1)
        self.metabolic_mult_spin.setValue(1.0)
        form.addRow(
            "Metabolic multiplier", self.metabolic_mult_spin
        )

        self.interruptibility_combo = QComboBox()
        for option in Interruptibility:
            self.interruptibility_combo.addItem(
                option.value, option
            )
        form.addRow(
            "Interruptibility", self.interruptibility_combo
        )

        self.min_lighting_spin = QSpinBox()
        self.min_lighting_spin.setRange(0, 10_000)
        form.addRow("Min lighting", self.min_lighting_spin)

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

    def _on_accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(
                self,
                "Name required",
                "Give the preset a name.",
            )
            return

        if not self.activity_combo.currentText():
            QMessageBox.warning(
                self,
                "Activity required",
                "Choose the physical activity this preset performs.",
            )
            return

        self.accept()

    def _add_technicality(self):
        technicality = (
            TechnicalityFormDialog.get_technicality(self)
        )
        if technicality is None:
            return
        if technicality.key in self.technicalities:
            QMessageBox.warning(
                self,
                "Duplicate key",
                f"A technicality with key '{technicality.key}' "
                "already exists.",
            )
            return
        self.technicalities[technicality.key] = technicality
        self._refresh_technicalities_table()

    def _edit_technicality_row(self, row, _column):
        key_item = self.technicalities_table.item(row, 0)
        if key_item is None:
            return
        original_key = key_item.text()
        existing = self.technicalities.get(original_key)
        if existing is None:
            return

        technicality = (
            TechnicalityFormDialog.get_technicality(
                self, existing=existing
            )
        )
        if technicality is None:
            return
        if (
            technicality.key != original_key
            and technicality.key in self.technicalities
        ):
            QMessageBox.warning(
                self,
                "Duplicate key",
                f"A technicality with key '{technicality.key}' "
                "already exists.",
            )
            return

        del self.technicalities[original_key]
        self.technicalities[technicality.key] = technicality
        self._refresh_technicalities_table()

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
                self.technicalities.pop(
                    key_item.text(), None
                )
        self._refresh_technicalities_table()

    def _refresh_technicalities_table(self):
        self.technicalities_table.setRowCount(0)
        for technicality in self.technicalities.values():
            row = self.technicalities_table.rowCount()
            self.technicalities_table.insertRow(row)
            for col, text in enumerate(
                (
                    technicality.key,
                    technicality.explanation,
                    technicality.trigger_handle,
                    technicality.trigger_policy.value,
                    (
                        f"{technicality.trigger_time}%"
                        if technicality.trigger_policy
                        is _ONCE
                        else "—"
                    ),
                )
            ):
                self.technicalities_table.setItem(
                    row, col, QTableWidgetItem(text)
                )

    def build_task_preset(self) -> TaskPreset:
        return TaskPreset(
            name=self.name_edit.text().strip(),
            skill_track=self.skill_track_combo.currentData(),
            activity=self._activities[
                self.activity_combo.currentText()
            ],
            # Rounded so slider float noise (0.30000000000000004) doesn't
            # end up in the generated task_presets.py file.
            tool_mode=self.tool_mode_combo.currentData(),
            metabolic_mult=self.metabolic_mult_spin.value(),
            min_lighting=self.min_lighting_spin.value(),
            technicalities=dict(self.technicalities),
            interruptibility=self.interruptibility_combo.currentData(),
            notes=self.notes_edit.toPlainText(),
        )

    @classmethod
    def get_task_preset(cls, parent=None):
        dialog = cls(parent)
        if dialog.exec():
            return dialog.build_task_preset()
        return None
