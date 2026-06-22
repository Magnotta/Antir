from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)


class LocalityEditorDialog(QDialog):
    def __init__(self, repo, locality=None, parent=None):
        super().__init__(parent)
        self.repo = repo
        self.locality = locality
        self.setWindowTitle(
            "Edit Locality"
            if self.locality
            else "New Locality"
        )
        self.setModal(True)
        self.resize(400, 300)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Tags (comma separated):"))
        self.tags_edit = QLineEdit()
        layout.addWidget(self.tags_edit)
        layout.addWidget(QLabel("Description:"))
        self.desc_edit = QTextEdit()
        layout.addWidget(self.desc_edit)
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        if self.locality:
            self._populate_fields()

    def _populate_fields(self):
        self.name_edit.setText(self.locality.name)
        self.tags_edit.setText(self.locality.tags or "")
        self.desc_edit.setText(
            self.locality.description or ""
        )

    def get_data(self):
        return {
            "name": self.name_edit.text().strip(),
            "tags": self.tags_edit.text().strip(),
            "description": self.desc_edit.toPlainText().strip(),
        }
