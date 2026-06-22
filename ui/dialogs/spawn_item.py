from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QDialog,
    QFormLayout,
    QDoubleSpinBox,
    QLabel,
)
from db.models.item import Mold
from db.repository.item import ItemRepository


class SpawnItemDialog(QDialog):
    def __init__(
        self,
        item_repo: ItemRepository,
        mold: Mold,
        parent=None,
    ):
        super().__init__(parent)
        self.mold = mold
        self.manual_fields: dict[str, QDoubleSpinBox] = {}
        self.setWindowTitle(f"Spawn Item – {mold.name}")
        self.setModal(True)
        layout = QVBoxLayout(self)
        info = QLabel(
            "Fill in the required parameters for this item."
        )
        info.setWordWrap(True)
        layout.addWidget(info)
        form = QFormLayout()
        for (
            param_dict
        ) in item_repo.get_manual_param_defaults(mold):
            spin = QDoubleSpinBox()
            spin.setDecimals(0)
            spin.setRange(0, param_dict["max"])
            spin.setValue(param_dict["value"])
            self.manual_fields[param_dict["param"]] = spin
            form.addRow(param_dict["param"], spin)
        if not self.manual_fields:
            form.addRow(
                QLabel("No manual parameters required.")
            )
        layout.addLayout(form)
        btn_spawn = QPushButton("Spawn")
        btn_cancel = QPushButton("Cancel")
        btn_spawn.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(btn_cancel)
        btns.addWidget(btn_spawn)
        layout.addLayout(btns)

    def get_manual_params(self) -> dict[str, int]:
        return {
            param: widget.value()
            for param, widget in self.manual_fields.items()
        }
