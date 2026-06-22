from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QLabel,
    QTextEdit,
    QDoubleSpinBox,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QSpinBox,
    QFormLayout,
)
from db.models.world import (
    PointCondition,
    SegmentCondition,
)
from core.defs import (
    PATH_CONDITION_KINDS,
    STR_PATH_COND_PARAMS,
    SEGM_COND_KINDS,
)


class ConditionEditorDialog(QDialog):
    def __init__(
        self,
        path_id: int,
        condition: PointCondition | SegmentCondition = None,
        parent=None,
    ):
        super().__init__(parent)
        self.path_id = path_id
        self.condition = condition
        self.param_widgets = {}
        self.setWindowTitle(
            "Edit Condition"
            if self.condition
            else "Add Condition"
        )
        self.setModal(True)
        self.resize(420, 350)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("Condition Type:"))
        self.kind_combo = QComboBox()
        self.kind_combo.addItems(
            PATH_CONDITION_KINDS.keys()
        )
        self.layout.addWidget(self.kind_combo)
        self.position_container = QWidget()
        self.position_layout = QFormLayout(
            self.position_container
        )
        self.layout.addWidget(self.position_container)

        # -------------------------------------
        # Dynamic Position Form
        # -------------------------------------
        self.position_container = QWidget()
        self.position_layout = QFormLayout(
            self.position_container
        )
        self.layout.addWidget(self.position_container)

        # =========================================================
        # Dynamic Parameter Form
        # =========================================================

        self.param_container = QWidget()
        self.param_form = QFormLayout(self.param_container)
        self.layout.addWidget(self.param_container)

        self.layout.addWidget(
            QLabel("Description (optional):")
        )
        self.desc_edit = QTextEdit()
        self.layout.addWidget(self.desc_edit)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(btn_layout)
        self.save_btn.clicked.connect(
            self._validate_and_accept
        )
        self.cancel_btn.clicked.connect(self.reject)
        self.kind_combo.currentTextChanged.connect(
            self._rebuild_all_dynamic_sections
        )
        if self.condition:
            self._populate_fields()
        else:
            self._rebuild_all_dynamic_sections()

    def _rebuild_all_dynamic_sections(self):
        self._rebuild_position_section()
        self._rebuild_param_section()

    def _clear_form_layout(self, form_layout):
        while form_layout.rowCount():
            form_layout.removeRow(0)

    def _rebuild_position_section(self):
        self._clear_form_layout(self.position_layout)
        kind = self.kind_combo.currentText()
        is_segment = kind in SEGM_COND_KINDS
        if is_segment:
            self.start_spin = QDoubleSpinBox()
            self.start_spin.setRange(0.0, 1.0)
            self.start_spin.setDecimals(3)
            self.end_spin = QDoubleSpinBox()
            self.end_spin.setRange(0.0, 1.0)
            self.end_spin.setDecimals(3)
            self.position_layout.addRow(
                "Start (0-1):", self.start_spin
            )
            self.position_layout.addRow(
                "End (0-1):", self.end_spin
            )
        else:
            self.position_spin = QDoubleSpinBox()
            self.position_spin.setRange(0.0, 1.0)
            self.position_spin.setDecimals(3)
            self.position_layout.addRow(
                "Position (0-1):", self.position_spin
            )

    def _rebuild_param_section(self):
        self._clear_form_layout(self.param_form)
        self.param_widgets.clear()
        kind = self.kind_combo.currentText()
        params = PATH_CONDITION_KINDS.get(kind, [])
        for param in params:
            if param in STR_PATH_COND_PARAMS.keys():
                widget = QComboBox()
                widget.addItems(STR_PATH_COND_PARAMS[param])
            else:
                widget = QSpinBox()
                widget.setRange(0, 10000)
            self.param_form.addRow(
                param.capitalize() + ":", widget
            )
            self.param_widgets[param] = widget

    def _populate_fields(self):
        self.kind_combo.setCurrentText(self.condition.kind)
        self._rebuild_all_dynamic_sections()
        if self.condition.kind in SEGM_COND_KINDS:
            self.start_spin.setValue(self.condition.start)
            self.end_spin.setValue(self.condition.end)
        else:
            self.position_spin.setValue(
                self.condition.position
            )
        data = self.condition.data or {}
        for param, widget in self.param_widgets.items():
            if param not in data:
                continue
            if isinstance(widget, QSpinBox):
                widget.setValue(int(data[param]))
            else:
                widget.setText(str(data[param]))

    def get_data(self):
        kind = self.kind_combo.currentText()
        is_segment = kind in SEGM_COND_KINDS
        data = {}
        for param, widget in self.param_widgets.items():
            if isinstance(widget, QSpinBox):
                data[param] = widget.value()
            else:
                data[param] = widget.text().strip()
        result = {
            "path_id": self.path_id,
            "kind": kind,
            "data": data,
            "description": self.desc_edit.toPlainText(),
        }
        if is_segment:
            result["start"] = self.start_spin.value()
            result["end"] = self.end_spin.value()
        else:
            result["position"] = self.position_spin.value()
        return result

    def _validate_and_accept(self):
        kind = self.kind_combo.currentText()
        is_segment = kind in SEGM_COND_KINDS
        if is_segment:
            if (
                self.start_spin.value()
                > self.end_spin.value()
            ):
                QMessageBox.warning(
                    self,
                    "Invalid Interval",
                    "Start must be <= End.",
                )
                return
        self.accept()
