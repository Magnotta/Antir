from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QDialog,
    QFormLayout,
    QDoubleSpinBox,
)
from db.models.item import ParamSpec
from core.defs import (
    ITEM_PARAM_MAXES,
)


class ParamSpecEditor(QDialog):
    def __init__(self, spec: ParamSpec, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Parameter Spec")
        self.param_edit = QLineEdit()
        self.base_edit = QDoubleSpinBox()
        self.base_edit.setRange(
            0, ITEM_PARAM_MAXES[spec.param]
        )
        self.base_edit.setDecimals(0)
        self.var_edit = QDoubleSpinBox()
        self.var_edit.setRange(
            0, ITEM_PARAM_MAXES[spec.param]
        )
        self.var_edit.setDecimals(0)
        form = QFormLayout()
        form.addRow("Param", self.param_edit)
        form.addRow("Base", self.base_edit)
        form.addRow("Variance", self.var_edit)
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(btn_cancel)
        btns.addWidget(btn_ok)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(btns)
        if spec:
            self.param_edit.setText(spec.param)
            self.base_edit.setValue(spec.base)
            self.var_edit.setValue(spec.variance)

    def get_data(self):
        return dict(
            param=self.param_edit.text().strip(),
            base=self.base_edit.value(),
            variance=self.var_edit.value(),
        )
