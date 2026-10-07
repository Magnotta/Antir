# # """
# # CreateTaskPresetDialog: builds a TaskPreset.

# # Mirrors TaskSpecDialog's pattern: build_task_preset() constructs the
# # dataclass from the widgets, get_task_preset() runs the dialog modally and
# # returns the built preset (or None if cancelled). This dialog doesn't save
# # anything itself -- same division of labor as TaskSpecDialog not saving the
# # TaskSpec it builds. Wiring it into the "Create Task Preset..." button looks
# # like:

# #     preset = CreateTaskPresetDialog.get_task_preset(self)
# #     if preset is not None:
# #         updated = add_preset(preset)
# #         self.preset_list.set_presets(updated)
# # """

# # from PyQt6.QtWidgets import QHeaderView
# # from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QTableWidget, QComboBox, QHBoxLayout, QVBoxLayout, QLabel, QPlainTextEdit, QSpinBox, QPushButton, QDialogButtonBox, QTableWidgetItem, QMessageBox
# # from core.defs import SkillTrack
# # from systems.task_service.task import TaskPreset, Interruptibility
# # from systems.task_service.physical_activities import PHYSICAL_ACTIVITIES_DICT
# # from ui.widgets.float_slider import FloatSlider

# # EXP_EFFECT_LABELS = ["Intensity", "Efficiency", "Quality", "Safety"]


# # class CreateTaskPresetDialog(QDialog):
# #     def __init__(self, parent=None):
# #         super().__init__(parent)
# #         self.setWindowTitle("Create Task Preset")

# #         form = QFormLayout(self)

# #         self.name_edit = QLineEdit()
# #         form.addRow("Name", self.name_edit)

# #         self.skill_track_combo = QComboBox()
# #         for option in SkillTrack:
# #             self.skill_track_combo.addItem(option.value, option)
# #         form.addRow("Skill track", self.skill_track_combo)

# #         # --- task_components: dict[str, float] --------------------------
# #         self.components_table = QTableWidget(0, 2)
# #         self.components_table.setHorizontalHeaderLabels(
# #             ["component", "weight"]
# #         )
# #         self.components_table.horizontalHeader().setSectionResizeMode(
# #             0, QHeaderView.ResizeMode.Stretch
# #         )
# #         self.components_table.setMaximumHeight(120)
# #         form.addRow("Task components", self.components_table)

# #         component_buttons = QHBoxLayout()
# #         add_component_button = QPushButton("+ Add Component")
# #         add_component_button.clicked.connect(self._add_component_row)
# #         remove_component_button = QPushButton(
# #             "Remove Selected"
# #         )
# #         remove_component_button.clicked.connect(
# #             self._remove_component_row
# #         )
# #         component_buttons.addWidget(add_component_button)
# #         component_buttons.addWidget(remove_component_button)
# #         form.addRow("", component_buttons)

# #         # --- exp_effect: tuple[float, float, float, float] ---------------
# #         self.exp_effect_sliders = []
# #         exp_col = QVBoxLayout()
# #         for label in EXP_EFFECT_LABELS:
# #             slider = FloatSlider(
# #                 minimum=-1000.0,
# #                 maximum=1000.0,
# #                 step=0.05,
# #                 value=0.0,
# #                 decimals=2,
# #             )
# #             self.exp_effect_sliders.append(slider)
# #             exp_row = QHBoxLayout()
# #             label_widget = QLabel(label)
# #             label_widget.setFixedWidth(70)
# #             exp_row.addWidget(label_widget)
# #             exp_row.addWidget(slider, stretch=1)
# #             exp_col.addLayout(exp_row)
# #         form.addRow("Exp effect", exp_col)

# #         self.base_workload_spin = QSpinBox()
# #         self.base_workload_spin.setRange(0, 1_000_000)
# #         form.addRow("Base workload", self.base_workload_spin)

# #         self.interruptibility_combo = QComboBox()
# #         for option in Interruptibility:
# #             self.interruptibility_combo.addItem(option.value, option)
# #         form.addRow("Interruptibility", self.interruptibility_combo)

# #         self.min_lighting_spin = QSpinBox()
# #         self.min_lighting_spin.setRange(0, 100)
# #         form.addRow("Min lighting", self.min_lighting_spin)

# #         self.notes_edit = QPlainTextEdit()
# #         self.notes_edit.setMaximumHeight(60)
# #         form.addRow("Notes", self.notes_edit)

# #         buttons = QDialogButtonBox(
# #             QDialogButtonBox.StandardButton.Ok
# #             | QDialogButtonBox.StandardButton.Cancel
# #         )
# #         buttons.accepted.connect(self._on_accept)
# #         buttons.rejected.connect(self.reject)
# #         form.addRow(buttons)

# #     def _on_accept(self):
# #         if not self.name_edit.text().strip():
# #             QMessageBox.warning(
# #                 self, "Name required", "Give the preset a name."
# #             )
# #             return

# #         components = self._task_components()
# #         total_weight = sum(components.values())
# #         if not abs(total_weight - 1.0) < 1e-6:
# #             QMessageBox.warning(
# #                 self,
# #                 "Weights must sum to 1.0",
# #                 "Task component weights must add up to 1.0 "
# #                 f"(currently {total_weight:.4f}).",
# #             )
# #             return

# #         self.accept()

# #     def _add_component_row(self):
# #         row = self.components_table.rowCount()
# #         self.components_table.insertRow(row)

# #         name_combo = QComboBox()
# #         for activity_name in PHYSICAL_ACTIVITIES_DICT.keys():
# #             name_combo.addItem(activity_name)
# #         self.components_table.setCellWidget(row, 0, name_combo)

# #         self.components_table.setItem(
# #             row, 1, QTableWidgetItem("1.0")
# #         )

# #     def _remove_component_row(self):
# #         for row in sorted(
# #             {i.row() for i in self.components_table.selectedIndexes()},
# #             reverse=True,
# #         ):
# #             self.components_table.removeRow(row)

# #     def _task_components(self) -> dict[str, float]:
# #         components = {}
# #         for row in range(self.components_table.rowCount()):
# #             name_combo = self.components_table.cellWidget(row, 0)
# #             weight_item = self.components_table.item(row, 1)
# #             name = name_combo.currentText().strip() if name_combo else ""
# #             if not name:
# #                 continue
# #             weight_text = weight_item.text() if weight_item else ""
# #             components[name] = float(weight_text) if weight_text else 0.0
# #         return components

# #     def build_task_preset(self) -> TaskPreset:
# #         return TaskPreset(
# #             name=self.name_edit.text().strip(),
# #             skill_track=self.skill_track_combo.currentData(),
# #             task_components=self._task_components(),
# #             exp_effect=tuple(
# #                 slider.value() for slider in self.exp_effect_sliders
# #             ),
# #             base_workload=self.base_workload_spin.value(),
# #             notes=self.notes_edit.toPlainText(),
# #             interruptibility=self.interruptibility_combo.currentData(),
# #             min_lighting=self.min_lighting_spin.value(),
# #         )

# #     @classmethod
# #     def get_task_preset(cls, parent=None):
# #         dialog = cls(parent)
# #         if dialog.exec():
# #             return dialog.build_task_preset()
# #         return None

# """
# CreateTaskPresetDialog: builds a TaskPreset.

# Mirrors TaskSpecDialog's pattern: build_task_preset() constructs the
# dataclass from the widgets, get_task_preset() runs the dialog modally and
# returns the built preset (or None if cancelled). This dialog doesn't save
# anything itself -- same division of labor as TaskSpecDialog not saving the
# TaskSpec it builds. Wiring it into the "Create Task Preset..." button looks
# like:

#     preset = CreateTaskPresetDialog.get_task_preset(self)
#     if preset is not None:
#         updated = add_preset(preset)
#         self.preset_list.set_presets(updated)
# """

# from PyQt6.QtWidgets import QHeaderView
# from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QTableWidget, QComboBox, QHBoxLayout, QVBoxLayout, QLabel, QPlainTextEdit, QSpinBox, QPushButton, QDialogButtonBox, QTableWidgetItem, QMessageBox
# from core.defs import SkillTrack
# from systems.task_service.task import TaskPreset, Interruptibility, Technicality
# from systems.task_service.physical_activities import PHYSICAL_ACTIVITIES_DICT
# from ui.widgets.float_slider import FloatSlider

# EXP_EFFECT_LABELS = ["Intensity", "Efficiency", "Quality", "Safety"]


# class CreateTaskPresetDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Create Task Preset")

#         form = QFormLayout(self)

#         self.name_edit = QLineEdit()
#         form.addRow("Name", self.name_edit)

#         self.skill_track_combo = QComboBox()
#         for option in SkillTrack:
#             self.skill_track_combo.addItem(option.value, option)
#         form.addRow("Skill track", self.skill_track_combo)

#         # --- task_components: dict[str, float] --------------------------
#         self.components_table = QTableWidget(0, 2)
#         self.components_table.setHorizontalHeaderLabels(
#             ["component", "weight"]
#         )
#         self.components_table.horizontalHeader().setSectionResizeMode(
#             0, QHeaderView.ResizeMode.Stretch
#         )
#         self.components_table.setMaximumHeight(120)
#         form.addRow("Task components", self.components_table)

#         component_buttons = QHBoxLayout()
#         add_component_button = QPushButton("+ Add Component")
#         add_component_button.clicked.connect(self._add_component_row)
#         remove_component_button = QPushButton(
#             "Remove Selected"
#         )
#         remove_component_button.clicked.connect(
#             self._remove_component_row
#         )
#         component_buttons.addWidget(add_component_button)
#         component_buttons.addWidget(remove_component_button)
#         form.addRow("", component_buttons)

#         # --- exp_effect: tuple[float, float, float, float] ---------------
#         self.exp_effect_sliders = []
#         exp_col = QVBoxLayout()
#         for label in EXP_EFFECT_LABELS:
#             slider = FloatSlider(
#                 minimum=-1000.0,
#                 maximum=1000.0,
#                 step=0.05,
#                 value=0.0,
#                 decimals=2,
#             )
#             self.exp_effect_sliders.append(slider)
#             exp_row = QHBoxLayout()
#             label_widget = QLabel(label)
#             label_widget.setFixedWidth(70)
#             exp_row.addWidget(label_widget)
#             exp_row.addWidget(slider, stretch=1)
#             exp_col.addLayout(exp_row)
#         form.addRow("Exp effect", exp_col)

#         # --- technicalities: dict[str, Technicality] ----------------------
#         self.technicalities_table = QTableWidget(0, 4)
#         self.technicalities_table.setHorizontalHeaderLabels(
#             ["type", "explanation", "threshold", "weight"]
#         )
#         self.technicalities_table.setMaximumHeight(120)
#         form.addRow("Technicalities", self.technicalities_table)

#         technicality_buttons = QHBoxLayout()
#         add_technicality_button = QPushButton("+ Add Technicality")
#         add_technicality_button.clicked.connect(
#             self._add_technicality_row
#         )
#         remove_technicality_button = QPushButton("Remove Selected")
#         remove_technicality_button.clicked.connect(
#             self._remove_technicality_row
#         )
#         technicality_buttons.addWidget(add_technicality_button)
#         technicality_buttons.addWidget(remove_technicality_button)
#         form.addRow("", technicality_buttons)

#         self.base_workload_spin = QSpinBox()
#         self.base_workload_spin.setRange(0, 1_000_000)
#         form.addRow("Base workload", self.base_workload_spin)

#         self.interruptibility_combo = QComboBox()
#         for option in Interruptibility:
#             self.interruptibility_combo.addItem(option.value, option)
#         form.addRow("Interruptibility", self.interruptibility_combo)

#         self.min_lighting_spin = QSpinBox()
#         self.min_lighting_spin.setRange(0, 100)
#         form.addRow("Min lighting", self.min_lighting_spin)

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

#     def _on_accept(self):
#         if not self.name_edit.text().strip():
#             QMessageBox.warning(
#                 self, "Name required", "Give the preset a name."
#             )
#             return

#         components = self._task_components()
#         total_weight = sum(components.values())
#         if not abs(total_weight - 1.0) < 1e-6:
#             QMessageBox.warning(
#                 self,
#                 "Weights must sum to 1.0",
#                 "Task component weights must add up to 1.0 "
#                 f"(currently {total_weight:.4f}).",
#             )
#             return

#         self.accept()

#     def _add_component_row(self):
#         row = self.components_table.rowCount()
#         self.components_table.insertRow(row)

#         name_combo = QComboBox()
#         for activity_name in PHYSICAL_ACTIVITIES_DICT.keys():
#             name_combo.addItem(activity_name)
#         self.components_table.setCellWidget(row, 0, name_combo)

#         self.components_table.setItem(
#             row, 1, QTableWidgetItem("1.0")
#         )

#     def _remove_component_row(self):
#         for row in sorted(
#             {i.row() for i in self.components_table.selectedIndexes()},
#             reverse=True,
#         ):
#             self.components_table.removeRow(row)

#     def _add_technicality_row(self):
#         row = self.technicalities_table.rowCount()
#         self.technicalities_table.insertRow(row)
#         self.technicalities_table.setItem(row, 0, QTableWidgetItem(""))
#         self.technicalities_table.setItem(row, 1, QTableWidgetItem(""))
#         self.technicalities_table.setItem(
#             row, 2, QTableWidgetItem("0.0")
#         )
#         self.technicalities_table.setItem(
#             row, 3, QTableWidgetItem("1.0")
#         )

#     def _remove_technicality_row(self):
#         for row in sorted(
#             {
#                 i.row()
#                 for i in self.technicalities_table.selectedIndexes()
#             },
#             reverse=True,
#         ):
#             self.technicalities_table.removeRow(row)

#     def _technicalities(self) -> dict[str, Technicality]:
#         technicalities = {}
#         for row in range(self.technicalities_table.rowCount()):
#             def cell(col, default=""):
#                 item = self.technicalities_table.item(row, col)
#                 return item.text() if item and item.text() else default

#             technicality_type = cell(0).strip()
#             if not technicality_type:
#                 continue
#             technicalities[technicality_type] = Technicality(
#                 type=technicality_type,
#                 explanation=cell(1),
#                 threshold=float(cell(2, "0.0")),
#                 weight=float(cell(3, "1.0")),
#             )
#         return technicalities

#     def _task_components(self) -> dict[str, float]:
#         components = {}
#         for row in range(self.components_table.rowCount()):
#             name_combo = self.components_table.cellWidget(row, 0)
#             weight_item = self.components_table.item(row, 1)
#             name = name_combo.currentText().strip() if name_combo else ""
#             if not name:
#                 continue
#             weight_text = weight_item.text() if weight_item else ""
#             components[name] = float(weight_text) if weight_text else 0.0
#         return components

#     def build_task_preset(self) -> TaskPreset:
#         return TaskPreset(
#             name=self.name_edit.text().strip(),
#             skill_track=self.skill_track_combo.currentData(),
#             task_components=self._task_components(),
#             exp_effect=tuple(
#                 slider.value() for slider in self.exp_effect_sliders
#             ),
#             base_workload=self.base_workload_spin.value(),
#             notes=self.notes_edit.toPlainText(),
#             interruptibility=self.interruptibility_combo.currentData(),
#             min_lighting=self.min_lighting_spin.value(),
#             technicalities=self._technicalities(),
#         )

#     @classmethod
#     def get_task_preset(cls, parent=None):
#         dialog = cls(parent)
#         if dialog.exec():
#             return dialog.build_task_preset()
#         return None

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
    QVBoxLayout,
    QLabel,
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
from core.defs import SkillTrack
from systems.task_service.task import (
    Interruptibility,
    Technicality,
)
from systems.task_service.task_presets import TaskPreset
from systems.task_service.physical_activities import (
    PHYSICAL_ACTIVITIES_DICT,
)
from ui.widgets.float_slider import FloatSlider

EXP_EFFECT_LABELS = [
    "Intensity",
    "Efficiency",
    "Quality",
    "Safety",
]


class TechnicalityFormDialog(QDialog):
    """Small popup form for creating or editing a single Technicality."""

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

        self.type_edit = QLineEdit()
        form.addRow("Type", self.type_edit)

        self.explanation_edit = QPlainTextEdit()
        self.explanation_edit.setMaximumHeight(60)
        form.addRow("Explanation", self.explanation_edit)

        self.threshold_spin = QDoubleSpinBox()
        self.threshold_spin.setRange(
            -1_000_000.0, 1_000_000.0
        )
        self.threshold_spin.setDecimals(3)
        form.addRow("Threshold", self.threshold_spin)

        self.weight_spin = QDoubleSpinBox()
        self.weight_spin.setRange(0.0, 1_000_000.0)
        self.weight_spin.setDecimals(3)
        self.weight_spin.setValue(1.0)
        form.addRow("Weight", self.weight_spin)

        if existing is not None:
            self.type_edit.setText(existing.type)
            self.explanation_edit.setPlainText(
                existing.explanation
            )
            self.threshold_spin.setValue(existing.threshold)
            self.weight_spin.setValue(existing.weight)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _on_accept(self):
        if not self.type_edit.text().strip():
            QMessageBox.warning(
                self,
                "Type required",
                "Give the technicality a type.",
            )
            return
        self.accept()

    def build_technicality(self) -> Technicality:
        return Technicality(
            type=self.type_edit.text().strip(),
            explanation=self.explanation_edit.toPlainText(),
            threshold=self.threshold_spin.value(),
            weight=self.weight_spin.value(),
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

        # --- task_components: dict[str, float] --------------------------
        self.components_table = QTableWidget(0, 2)
        self.components_table.setHorizontalHeaderLabels(
            ["component", "weight"]
        )
        self.components_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.components_table.setMaximumHeight(120)
        form.addRow(
            "Task components", self.components_table
        )

        component_buttons = QHBoxLayout()
        add_component_button = QPushButton(
            "+ Add Component"
        )
        add_component_button.clicked.connect(
            self._add_component_row
        )
        remove_component_button = QPushButton(
            "Remove Selected"
        )
        remove_component_button.clicked.connect(
            self._remove_component_row
        )
        component_buttons.addWidget(add_component_button)
        component_buttons.addWidget(remove_component_button)
        form.addRow("", component_buttons)

        # --- exp_effect: tuple[float, float, float, float] ---------------
        self.exp_effect_sliders = []
        exp_col = QVBoxLayout()
        for label in EXP_EFFECT_LABELS:
            slider = FloatSlider(
                minimum=-1.0,
                maximum=10.0,
                step=0.004,
                value=0.0,
                decimals=2,
            )
            self.exp_effect_sliders.append(slider)
            exp_row = QHBoxLayout()
            label_widget = QLabel(label)
            label_widget.setFixedWidth(70)
            exp_row.addWidget(label_widget)
            exp_row.addWidget(slider, stretch=1)
            exp_col.addLayout(exp_row)
        form.addRow("Exp effect", exp_col)

        # --- technicalities: dict[str, Technicality] ----------------------
        self.technicalities: dict[str, Technicality] = {}
        self.technicalities_table = QTableWidget(0, 4)
        self.technicalities_table.setHorizontalHeaderLabels(
            ["type", "explanation", "thresh", "weight"]
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

        self.base_workload_spin = QSpinBox()
        self.base_workload_spin.setRange(0, 100_000)
        form.addRow(
            "Base workload", self.base_workload_spin
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

        components = self._task_components()
        total_weight = sum(components.values())
        if not abs(total_weight - 1.0) < 1e-6:
            QMessageBox.warning(
                self,
                "Weights must sum to 1.0",
                "Task component weights must add up to 1.0 "
                f"(currently {total_weight:.4f}).",
            )
            return

        self.accept()

    def _add_component_row(self):
        row = self.components_table.rowCount()
        self.components_table.insertRow(row)

        name_combo = QComboBox()
        for (
            activity_name
        ) in PHYSICAL_ACTIVITIES_DICT.keys():
            name_combo.addItem(activity_name)
        self.components_table.setCellWidget(
            row, 0, name_combo
        )

        self.components_table.setItem(
            row, 1, QTableWidgetItem("1.0")
        )

    def _remove_component_row(self):
        for row in sorted(
            {
                i.row()
                for i in self.components_table.selectedIndexes()
            },
            reverse=True,
        ):
            self.components_table.removeRow(row)

    def _add_technicality(self):
        technicality = (
            TechnicalityFormDialog.get_technicality(self)
        )
        if technicality is None:
            return
        if technicality.type in self.technicalities:
            QMessageBox.warning(
                self,
                "Duplicate type",
                f"A technicality of type '{technicality.type}' "
                "already exists.",
            )
            return
        self.technicalities[technicality.type] = (
            technicality
        )
        self._refresh_technicalities_table()

    def _edit_technicality_row(self, row, _column):
        type_item = self.technicalities_table.item(row, 0)
        if type_item is None:
            return
        original_type = type_item.text()
        existing = self.technicalities.get(original_type)
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
            technicality.type != original_type
            and technicality.type in self.technicalities
        ):
            QMessageBox.warning(
                self,
                "Duplicate type",
                f"A technicality of type '{technicality.type}' "
                "already exists.",
            )
            return

        del self.technicalities[original_type]
        self.technicalities[technicality.type] = (
            technicality
        )
        self._refresh_technicalities_table()

    def _remove_technicality_row(self):
        for row in sorted(
            {
                i.row()
                for i in self.technicalities_table.selectedIndexes()
            },
            reverse=True,
        ):
            type_item = self.technicalities_table.item(
                row, 0
            )
            if type_item is not None:
                self.technicalities.pop(
                    type_item.text(), None
                )
        self._refresh_technicalities_table()

    def _refresh_technicalities_table(self):
        self.technicalities_table.setRowCount(0)
        for technicality in self.technicalities.values():
            row = self.technicalities_table.rowCount()
            self.technicalities_table.insertRow(row)
            for col, text in enumerate(
                (
                    technicality.type,
                    technicality.explanation,
                    f"{technicality.threshold:g}",
                    f"{technicality.weight:g}",
                )
            ):
                self.technicalities_table.setItem(
                    row, col, QTableWidgetItem(text)
                )

    def _task_components(self) -> dict[str, float]:
        components = {}
        for row in range(self.components_table.rowCount()):
            name_combo = self.components_table.cellWidget(
                row, 0
            )
            weight_item = self.components_table.item(row, 1)
            name = (
                name_combo.currentText().strip()
                if name_combo
                else ""
            )
            if not name:
                continue
            weight_text = (
                weight_item.text() if weight_item else ""
            )
            components[name] = (
                float(weight_text) if weight_text else 0.0
            )
        return components

    def build_task_preset(self) -> TaskPreset:
        return TaskPreset(
            name=self.name_edit.text().strip(),
            skill_track=self.skill_track_combo.currentData(),
            task_components=self._task_components(),
            exp_effect=tuple(
                slider.value()
                for slider in self.exp_effect_sliders
            ),
            metabolic_mult=self.base_workload_spin.value(),
            notes=self.notes_edit.toPlainText(),
            interruptibility=self.interruptibility_combo.currentData(),
            min_lighting=self.min_lighting_spin.value(),
            technicalities=dict(self.technicalities),
        )

    @classmethod
    def get_task_preset(cls, parent=None):
        dialog = cls(parent)
        if dialog.exec():
            return dialog.build_task_preset()
        return None
