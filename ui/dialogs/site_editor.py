from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QComboBox,
    QSpinBox,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)

from db.models.world import Locality, Path, Site
from systems.location_service.site_preset_repository import (
    load_presets as load_site_presets,
)


class SiteEditorDialog(QDialog):
    """Create or edit a single Site, anchored to either a Locality or a
    Path (never both -- pass exactly one, or an existing `site`, which
    determines its own anchor)."""

    def __init__(
        self,
        repo,
        locality: Locality = None,
        path: Path = None,
        site: Site = None,
        parent=None,
    ):
        super().__init__(parent)
        self.repo = repo
        self.site = site

        if site is not None:
            self.locality = site.locality
            self.path = site.path
        else:
            self.locality = locality
            self.path = path

        if (self.locality is None) == (self.path is None):
            raise ValueError(
                "SiteEditorDialog needs exactly one of locality or path"
            )

        self.setWindowTitle(
            "Edit Site" if self.site else "Add Site"
        )
        self.setModal(True)
        self.resize(420, 340)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Site.name now doubles as the key into SITE_PRESETS_DICT, so this
        # is a combo of existing preset keys rather than free text --
        # nothing here can produce a dangling preset reference.
        layout.addWidget(QLabel("Preset:"))
        self.preset_combo = QComboBox()
        self.presets = load_site_presets()
        for key in self.presets:
            self.preset_combo.addItem(key)
        layout.addWidget(self.preset_combo)

        layout.addWidget(QLabel("Description:"))
        self.desc_edit = QTextEdit()
        layout.addWidget(self.desc_edit)

        if self.path is not None:
            layout.addWidget(QLabel("Start (m):"))
            self.start_spin = QSpinBox()
            self.start_spin.setRange(0, self.path.length_m)
            layout.addWidget(self.start_spin)

            layout.addWidget(QLabel("End (m):"))
            self.end_spin = QSpinBox()
            self.end_spin.setRange(0, self.path.length_m)
            layout.addWidget(self.end_spin)

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

        if self.site:
            self._populate_fields()

    def _populate_fields(self):
        index = self.preset_combo.findText(self.site.name)
        if index >= 0:
            self.preset_combo.setCurrentIndex(index)
        self.desc_edit.setText(self.site.description or "")
        if self.path is not None:
            self.start_spin.setValue(self.site.start or 0)
            self.end_spin.setValue(self.site.end or 0)

    def _validate_and_accept(self):
        if self.preset_combo.currentText() == "":
            QMessageBox.warning(
                self,
                "No Presets Available",
                "There are no site presets defined yet. Add one to "
                "site_presets.py before creating a site.",
            )
            return
        if (
            self.path is not None
            and self.start_spin.value()
            > self.end_spin.value()
        ):
            QMessageBox.warning(
                self,
                "Invalid Interval",
                "Start must be <= End.",
            )
            return
        self.accept()

    def get_data(self):
        data = {
            "name": self.preset_combo.currentText(),
            "description": self.desc_edit.toPlainText().strip(),
        }
        if self.locality is not None:
            data["locality"] = self.locality
        else:
            data["path"] = self.path
            data["start"] = self.start_spin.value()
            data["end"] = self.end_spin.value()
        return data
