from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QDoubleSpinBox,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)
from db.models.world import (
    Locality,
)


class PathEditorDialog(QDialog):
    def __init__(
        self, repo, origin: Locality, path=None, parent=None
    ):
        super().__init__(parent)
        self.repo = repo
        self.origin = origin
        self.path = path
        self.setWindowTitle(
            "Edit Path" if self.path else "Add Path"
        )
        self.setModal(True)
        self.resize(400, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.dest_label = QLabel("Destination:")
        self.layout.addWidget(self.dest_label)
        self.dest_combo = QComboBox()
        self.localities = self.repo.get_all_localities()
        for loc in self.localities:
            if loc != self.origin:
                self.dest_combo.addItem(loc.name, loc)
        self.layout.addWidget(self.dest_combo)
        self.distance_label = QLabel("Distance (km):")
        self.layout.addWidget(self.distance_label)
        self.distance_spin = QDoubleSpinBox()
        self.distance_spin.setRange(0, 100000)
        self.distance_spin.setDecimals(0)
        self.distance_spin.setValue(1)
        self.layout.addWidget(self.distance_spin)
        self.desc_label = QLabel("Description:")
        self.layout.addWidget(self.desc_label)
        self.desc_edit = QLineEdit()
        self.layout.addWidget(self.desc_edit)
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(button_layout)
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        if self.path:
            self._populate_fields()

    def _populate_fields(self):
        index = self.dest_combo.findData(
            self.path.destination_id
        )
        if index >= 0:
            self.dest_combo.setCurrentIndex(index)
        self.distance_spin.setValue(self.path.distance_km)
        self.desc_edit.setText(self.path.description or "")

    def get_data(self):
        return {
            "origin": self.origin,
            "destination": self.dest_combo.currentData(),
            "distance_km": self.distance_spin.value(),
            "description": self.desc_edit.text(),
        }
