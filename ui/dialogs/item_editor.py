from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QDialog,
    QTextEdit,
    QMessageBox,
    QFormLayout,
    QDoubleSpinBox,
)
from db.models.item import Item
from db.repository.item import ItemRepository


class ItemEditorDialog(QDialog):
    def __init__(
        self, item: Item, repo: ItemRepository, parent=None
    ):
        super().__init__(parent)
        self.item = item
        self.repo = repo
        self.inputs = {}
        self.setWindowTitle(f"Edit Item #{item.id}")
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.item.name)
        form.addRow("Name", self.name_edit)
        for param in self.item.param_list:
            spin = QDoubleSpinBox()
            spin.setMinimum(0)
            spin.setMaximum(self.repo.get_param_max(param))
            spin.setValue(param.value)
            spin.setDecimals(0)
            self.inputs[param.name] = spin
            form.addRow(param.name, spin)
        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(80)
        self.desc_edit.setText(self.item.description)
        form.addRow("Description", self.desc_edit)
        layout.addLayout(form)
        btns = QHBoxLayout()
        btns.addStretch()
        cancel = QPushButton("Cancel")
        save = QPushButton("Save")
        cancel.clicked.connect(self.reject)
        save.clicked.connect(self.on_save)
        btns.addWidget(cancel)
        btns.addWidget(save)
        layout.addLayout(btns)

    def on_save(self):
        try:
            for param, widget in self.inputs.items():
                value = widget.value()
                self._set_param(param, value)
            self.item.name = self.name_edit.text()
            self.item.description = (
                self.desc_edit.toPlainText()
            )
            self.repo.session.commit()
            self.accept()
        except Exception as e:
            self.repo.session.rollback()
            QMessageBox.critical(self, "Error", str(e))

    def _set_param(self, param, value):
        for p in self.item.param_list:
            if p.name == param:
                p.value = value
                return
