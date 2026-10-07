from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QComboBox,
    QSpinBox,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)

from db.models.world import Junction, Path


class JunctionEditorDialog(QDialog):
    """Create or edit a Junction connecting `path` (always treated as the
    "this path" side) to some other path, at a position on each.
    """

    def __init__(
        self,
        repo,
        path: Path,
        junction: Junction = None,
        parent=None,
    ):
        super().__init__(parent)
        self.repo = repo
        self.path = path
        self.junction = junction
        self.setWindowTitle(
            "Edit Junction"
            if self.junction
            else "Add Junction"
        )
        self.setModal(True)
        self.resize(420, 280)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(
            QLabel(
                f"This path: {self._path_label(self.path)}"
            )
        )

        layout.addWidget(
            QLabel("Position on this path (m):")
        )
        self.this_position_spin = QSpinBox()
        self.this_position_spin.setRange(
            0, self.path.length_m
        )
        layout.addWidget(self.this_position_spin)

        layout.addWidget(QLabel("Other path:"))
        self.other_path_combo = QComboBox()
        self.other_paths = [
            p
            for p in self.repo.get_all_paths()
            if p.id != self.path.id
        ]
        for p in self.other_paths:
            self.other_path_combo.addItem(
                self._path_label(p), p
            )
        layout.addWidget(self.other_path_combo)
        self.other_path_combo.currentIndexChanged.connect(
            self._reload_other_position_range
        )

        layout.addWidget(
            QLabel("Position on other path (m):")
        )
        self.other_position_spin = QSpinBox()
        layout.addWidget(self.other_position_spin)

        layout.addWidget(QLabel("Description:"))
        self.desc_edit = QLineEdit()
        layout.addWidget(self.desc_edit)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        self.save_btn.clicked.connect(
            self._validate_and_accept
        )
        self.cancel_btn.clicked.connect(self.reject)

        self._reload_other_position_range()
        if self.junction:
            self._populate_fields()

    @staticmethod
    def _path_label(path: Path) -> str:
        return (
            f"{path.origin.name} -> {path.destination.name}"
        )

    def _reload_other_position_range(self):
        other_path = self.other_path_combo.currentData()
        if other_path is None:
            self.other_position_spin.setRange(0, 0)
            return
        self.other_position_spin.setRange(
            0, other_path.length_m
        )

    def _populate_fields(self):
        other_path, other_position = (
            self.junction.other_path(self.path)
        )
        this_position = (
            self.junction.position_a_m
            if self.junction.path_a_id == self.path.id
            else self.junction.position_b_m
        )
        self.this_position_spin.setValue(this_position)
        index = self.other_path_combo.findData(other_path)
        if index >= 0:
            self.other_path_combo.setCurrentIndex(index)
        # currentIndexChanged only fires on an actual index change -- make
        # sure the range is right even if the found index was already 0.
        self._reload_other_position_range()
        self.other_position_spin.setValue(other_position)
        self.desc_edit.setText(
            self.junction.description or ""
        )

    def _validate_and_accept(self):
        if self.other_path_combo.currentData() is None:
            QMessageBox.warning(
                self,
                "No Other Path",
                "There is no other path to connect to yet.",
            )
            return
        self.accept()

    def get_data(self):
        # `path` is always stored as the "a" side and the selection as
        # "b" -- path_a/path_b are otherwise interchangeable in the model
        # (see Junction.other_path), so this doesn't affect correctness
        # even when editing a junction that was originally saved the
        # other way around.
        return {
            "path_a": self.path,
            "position_a_m": self.this_position_spin.value(),
            "path_b": self.other_path_combo.currentData(),
            "position_b_m": self.other_position_spin.value(),
            "description": self.desc_edit.text().strip(),
        }
