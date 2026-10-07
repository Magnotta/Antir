# # from PyQt6.QtWidgets import (
# #     QDialog,
# #     QLabel,
# #     QLineEdit,
# #     QTextEdit,
# #     QPushButton,
# #     QHBoxLayout,
# #     QVBoxLayout,
# # )


# # class LocalityEditorDialog(QDialog):
# #     def __init__(self, repo, locality=None, parent=None):
# #         super().__init__(parent)
# #         self.repo = repo
# #         self.locality = locality
# #         self.setWindowTitle(
# #             "Edit Locality"
# #             if self.locality
# #             else "New Locality"
# #         )
# #         self.setModal(True)
# #         self.resize(400, 300)
# #         layout = QVBoxLayout()
# #         self.setLayout(layout)
# #         layout.addWidget(QLabel("Name:"))
# #         self.name_edit = QLineEdit()
# #         layout.addWidget(self.name_edit)
# #         layout.addWidget(QLabel("Tags (comma separated):"))
# #         self.tags_edit = QLineEdit()
# #         layout.addWidget(self.tags_edit)
# #         layout.addWidget(QLabel("Description:"))
# #         self.desc_edit = QTextEdit()
# #         layout.addWidget(self.desc_edit)
# #         btn_layout = QHBoxLayout()
# #         self.save_btn = QPushButton("Save")
# #         self.cancel_btn = QPushButton("Cancel")
# #         btn_layout.addWidget(self.save_btn)
# #         btn_layout.addWidget(self.cancel_btn)
# #         layout.addLayout(btn_layout)
# #         self.save_btn.clicked.connect(self.accept)
# #         self.cancel_btn.clicked.connect(self.reject)
# #         if self.locality:
# #             self._populate_fields()

# #     def _populate_fields(self):
# #         self.name_edit.setText(self.locality.name)
# #         self.tags_edit.setText(self.locality.tags or "")
# #         self.desc_edit.setText(
# #             self.locality.description or ""
# #         )

# #     def get_data(self):
# #         return {
# #             "name": self.name_edit.text().strip(),
# #             "tags": self.tags_edit.text().strip(),
# #             "description": self.desc_edit.toPlainText().strip(),
# #         }

# from PyQt6.QtWidgets import (
#     QDialog,
#     QLabel,
#     QLineEdit,
#     QTextEdit,
#     QPushButton,
#     QHBoxLayout,
#     QVBoxLayout,
#     QTableWidget,
#     QTableWidgetItem,
#     QAbstractItemView,
#     QHeaderView,
#     QMessageBox,
#     QGroupBox,
# )

# from db.models.world import Locality, Site
# # from ui.dialogs.site_editor import SiteEditorDialog

# # Not yet written -- see the "expected SiteEditorDialog interface" note
# # above _add_site(). Adjust the import path once that file exists.
# #
# # Expected interface:
# #   SiteEditorDialog(repo, locality: Locality, site: Site = None, parent=None)
# #   .get_data() -> {"locality": Locality, "name": str, "description": str}
# #
# # Since Site.name now doubles as the key into SITE_PRESETS_DICT (per the
# # site-preset design), that dialog's "Name" field probably wants to be a
# # QComboBox populated from site_preset_repository.load_presets().keys()
# # rather than free text, to keep it from producing invalid preset keys.


# class LocalityEditorDialog(QDialog):
#     def __init__(
#         self, repo, locality: Locality = None, parent=None
#     ):
#         super().__init__(parent)
#         self.repo = repo
#         self.locality = locality
#         self._sites: list[Site] = (
#             list(self.locality.sites) if self.locality else []
#         )
#         self.setWindowTitle(
#             "Edit Locality"
#             if self.locality
#             else "New Locality"
#         )
#         self.setModal(True)
#         self.resize(480, 520)
#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         layout.addWidget(QLabel("Name:"))
#         self.name_edit = QLineEdit()
#         layout.addWidget(self.name_edit)

#         layout.addWidget(QLabel("Tags (comma separated):"))
#         self.tags_edit = QLineEdit()
#         layout.addWidget(self.tags_edit)

#         layout.addWidget(QLabel("Description:"))
#         self.desc_edit = QTextEdit()
#         layout.addWidget(self.desc_edit)

#         layout.addWidget(self._build_sites_group())

#         btn_layout = QHBoxLayout()
#         self.save_btn = QPushButton("Save")
#         self.cancel_btn = QPushButton("Cancel")
#         btn_layout.addWidget(self.save_btn)
#         btn_layout.addWidget(self.cancel_btn)
#         layout.addLayout(btn_layout)
#         self.save_btn.clicked.connect(self.accept)
#         self.cancel_btn.clicked.connect(self.reject)

#         if self.locality:
#             self._populate_fields()

#     # ------------------------------------------------------------------
#     # Sites
#     # ------------------------------------------------------------------

#     def _build_sites_group(self) -> QGroupBox:
#         group = QGroupBox("Sites")
#         group_layout = QVBoxLayout()
#         group.setLayout(group_layout)

#         self.sites_table = QTableWidget(0, 2)
#         self.sites_table.setHorizontalHeaderLabels(
#             ["Name", "Description"]
#         )
#         self.sites_table.horizontalHeader().setSectionResizeMode(
#             1, QHeaderView.ResizeMode.Stretch
#         )
#         self.sites_table.setEditTriggers(
#             QAbstractItemView.EditTrigger.NoEditTriggers
#         )
#         self.sites_table.setSelectionBehavior(
#             QAbstractItemView.SelectionBehavior.SelectRows
#         )
#         self.sites_table.setSelectionMode(
#             QAbstractItemView.SelectionMode.SingleSelection
#         )
#         self.sites_table.cellDoubleClicked.connect(
#             lambda *_: self._edit_selected_site()
#         )
#         group_layout.addWidget(self.sites_table)

#         btn_layout = QHBoxLayout()
#         self.add_site_btn = QPushButton("Add Site")
#         self.remove_site_btn = QPushButton("Remove Site")
#         btn_layout.addWidget(self.add_site_btn)
#         btn_layout.addWidget(self.remove_site_btn)
#         group_layout.addLayout(btn_layout)
#         self.add_site_btn.clicked.connect(self._add_site)
#         self.remove_site_btn.clicked.connect(
#             self._remove_selected_site
#         )

#         # A new locality has no id yet, so sites (which FK to it) can't
#         # be created until the locality itself is saved once.
#         if self.locality is None:
#             group.setEnabled(False)
#             group.setToolTip(
#                 "Save the locality first to add sites."
#             )

#         self._reload_sites_table()
#         return group

#     def _reload_sites_table(self):
#         self.sites_table.setRowCount(0)
#         for site in self._sites:
#             row = self.sites_table.rowCount()
#             self.sites_table.insertRow(row)
#             self.sites_table.setItem(
#                 row, 0, QTableWidgetItem(site.name)
#             )
#             self.sites_table.setItem(
#                 row,
#                 1,
#                 QTableWidgetItem(site.description or ""),
#             )

#     def _add_site(self):
#         # dialog = SiteEditorDialog(
#         #     self.repo, locality=self.locality, parent=self
#         # )
#         # if dialog.exec():
#         #     data = dialog.get_data()
#         #     site = self.repo.add_site(**data)
#         #     self._sites.append(site)
#         #     self._reload_sites_table()
#         pass

#     def _edit_selected_site(self):
#         # site = self._selected_site()
#         # if site is None:
#         #     return
#         # dialog = SiteEditorDialog(
#         #     self.repo,
#         #     locality=self.locality,
#         #     site=site,
#         #     parent=self,
#         # )
#         # if dialog.exec():
#         #     data = dialog.get_data()
#         #     self.repo.update_site(site.id, **data)
#         #     self._reload_sites_table()
#         pass

#     def _remove_selected_site(self):
#         site = self._selected_site()
#         if site is None:
#             return
#         confirm = QMessageBox.question(
#             self,
#             "Remove Site",
#             f"Remove site {site.name!r}? This cannot be undone.",
#             QMessageBox.StandardButton.Yes
#             | QMessageBox.StandardButton.No,
#         )
#         if confirm != QMessageBox.StandardButton.Yes:
#             return
#         self.repo.delete_site(site)
#         self._sites.remove(site)
#         self._reload_sites_table()

#     def _selected_site(self) -> Site | None:
#         row = self.sites_table.currentRow()
#         if row < 0 or row >= len(self._sites):
#             return None
#         return self._sites[row]

#     # ------------------------------------------------------------------
#     # Locality fields
#     # ------------------------------------------------------------------

#     def _populate_fields(self):
#         self.name_edit.setText(self.locality.name)
#         data = self.locality.data or {}
#         self.tags_edit.setText(", ".join(data.get("tags", [])))
#         self.desc_edit.setText(
#             self.locality.description or ""
#         )

#     def get_data(self):
#         tags = [
#             t.strip()
#             for t in self.tags_edit.text().split(",")
#             if t.strip()
#         ]
#         # Preserve any other keys already in `data` (tags is not
#         # necessarily the only thing that lives in there).
#         data = (
#             dict(self.locality.data)
#             if self.locality and self.locality.data
#             else {}
#         )
#         if tags:
#             data["tags"] = tags
#         else:
#             data.pop("tags", None)
#         return {
#             "name": self.name_edit.text().strip(),
#             "description": self.desc_edit.toPlainText().strip(),
#             "data": data or None,
#         }

from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QMessageBox,
    QGroupBox,
)

from db.models.world import Locality, Site
from ui.dialogs.site_editor import SiteEditorDialog


class LocalityEditorDialog(QDialog):
    def __init__(
        self, repo, locality: Locality = None, parent=None
    ):
        super().__init__(parent)
        self.repo = repo
        self.locality = locality
        self._sites: list[Site] = (
            list(self.locality.sites)
            if self.locality
            else []
        )
        self.setWindowTitle(
            "Edit Locality"
            if self.locality
            else "New Locality"
        )
        self.setModal(True)
        self.resize(480, 500)
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit)

        layout.addWidget(QLabel("Description:"))
        self.desc_edit = QTextEdit()
        layout.addWidget(self.desc_edit)

        self.sites_group = self._build_sites_group()
        layout.addWidget(self.sites_group)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.close_btn = QPushButton("Close")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.close_btn)
        layout.addLayout(btn_layout)
        # Save persists immediately but does NOT close the dialog -- a new
        # locality has to exist in the DB before sites (which FK to it)
        # can be added, and we want that to happen without a round trip
        # through closing and reopening this dialog. "Close" is the only
        # button that ends the dialog now; there is no more "discard my
        # changes" button, since Save may already have committed some of
        # them. Whatever code opens this dialog should stop calling
        # repo.add_locality/update_locality after exec() returns -- that
        # now happens inside the dialog itself, on each Save click.
        self.save_btn.clicked.connect(self._save)
        self.close_btn.clicked.connect(self.reject)

        if self.locality:
            self._populate_fields()

    # ------------------------------------------------------------------
    # Sites
    # ------------------------------------------------------------------

    def _build_sites_group(self) -> QGroupBox:
        group = QGroupBox("Sites")
        group_layout = QVBoxLayout()
        group.setLayout(group_layout)

        self.sites_table = QTableWidget(0, 2)
        self.sites_table.setHorizontalHeaderLabels(
            ["Name", "Description"]
        )
        self.sites_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.sites_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.sites_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.sites_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.sites_table.cellDoubleClicked.connect(
            lambda *_: self._edit_selected_site()
        )
        group_layout.addWidget(self.sites_table)

        btn_layout = QHBoxLayout()
        self.add_site_btn = QPushButton("Add Site")
        self.remove_site_btn = QPushButton("Remove Site")
        btn_layout.addWidget(self.add_site_btn)
        btn_layout.addWidget(self.remove_site_btn)
        group_layout.addLayout(btn_layout)
        self.add_site_btn.clicked.connect(self._add_site)
        self.remove_site_btn.clicked.connect(
            self._remove_selected_site
        )

        if self.locality is None:
            group.setEnabled(False)
            group.setToolTip(
                "Save the locality first to add sites."
            )

        self._reload_sites_table()
        return group

    def _reload_sites_table(self):
        self.sites_table.setRowCount(0)
        for site in self._sites:
            row = self.sites_table.rowCount()
            self.sites_table.insertRow(row)
            self.sites_table.setItem(
                row, 0, QTableWidgetItem(site.name)
            )
            self.sites_table.setItem(
                row,
                1,
                QTableWidgetItem(site.description or ""),
            )

    def _add_site(self):
        dialog = SiteEditorDialog(
            self.repo, locality=self.locality, parent=self
        )
        if dialog.exec():
            data = dialog.get_data()
            site = self.repo.add_site(**data)
            self._sites.append(site)
            self._reload_sites_table()

    def _edit_selected_site(self):
        site = self._selected_site()
        if site is None:
            return
        dialog = SiteEditorDialog(
            self.repo,
            locality=self.locality,
            site=site,
            parent=self,
        )
        if dialog.exec():
            data = dialog.get_data()
            self.repo.update_site(site.id, **data)
            self._reload_sites_table()

    def _remove_selected_site(self):
        site = self._selected_site()
        if site is None:
            return
        confirm = QMessageBox.question(
            self,
            "Remove Site",
            f"Remove site {site.name!r}? This cannot be undone.",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        self.repo.delete_site(site)
        self._sites.remove(site)
        self._reload_sites_table()

    def _selected_site(self) -> Site | None:
        row = self.sites_table.currentRow()
        if row < 0 or row >= len(self._sites):
            return None
        return self._sites[row]

    # ------------------------------------------------------------------
    # Locality fields
    # ------------------------------------------------------------------

    def _populate_fields(self):
        self.name_edit.setText(self.locality.name)
        self.desc_edit.setText(
            self.locality.description or ""
        )

    def get_data(self):
        return {
            "name": self.name_edit.text().strip(),
            "description": self.desc_edit.toPlainText().strip(),
        }

    def _save(self):
        data = self.get_data()
        if self.locality is None:
            self.locality = self.repo.add_locality(**data)
            self._sites = list(self.locality.sites)
            self.sites_group.setEnabled(True)
            self.sites_group.setToolTip("")
            self._reload_sites_table()
        else:
            self.repo.update_locality(
                self.locality.id, **data
            )
        self.setWindowTitle(
            f"Edit Locality — {self.locality.name}"
        )
