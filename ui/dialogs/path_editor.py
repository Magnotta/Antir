# # from PyQt6.QtWidgets import (
# #     QDialog,
# #     QLabel,
# #     QLineEdit,
# #     QDoubleSpinBox,
# #     QComboBox,
# #     QPushButton,
# #     QHBoxLayout,
# #     QVBoxLayout,
# # )
# # from db.models.world import (
# #     Locality,
# # )


# # class PathEditorDialog(QDialog):
# #     def __init__(
# #         self, repo, origin: Locality, path=None, parent=None
# #     ):
# #         super().__init__(parent)
# #         self.repo = repo
# #         self.origin = origin
# #         self.path = path
# #         self.setWindowTitle(
# #             "Edit Path" if self.path else "Add Path"
# #         )
# #         self.setModal(True)
# #         self.resize(400, 200)
# #         self.layout = QVBoxLayout()
# #         self.setLayout(self.layout)
# #         self.dest_label = QLabel("Destination:")
# #         self.layout.addWidget(self.dest_label)
# #         self.dest_combo = QComboBox()
# #         self.localities = self.repo.get_all_localities()
# #         for loc in self.localities:
# #             if loc != self.origin:
# #                 self.dest_combo.addItem(loc.name, loc)
# #         self.layout.addWidget(self.dest_combo)
# #         self.distance_label = QLabel("Distance (km):")
# #         self.layout.addWidget(self.distance_label)
# #         self.distance_spin = QDoubleSpinBox()
# #         self.distance_spin.setRange(0, 100000)
# #         self.distance_spin.setDecimals(0)
# #         self.distance_spin.setValue(1)
# #         self.layout.addWidget(self.distance_spin)
# #         self.desc_label = QLabel("Description:")
# #         self.layout.addWidget(self.desc_label)
# #         self.desc_edit = QLineEdit()
# #         self.layout.addWidget(self.desc_edit)
# #         button_layout = QHBoxLayout()
# #         self.save_btn = QPushButton("Save")
# #         self.cancel_btn = QPushButton("Cancel")
# #         button_layout.addWidget(self.save_btn)
# #         button_layout.addWidget(self.cancel_btn)
# #         self.layout.addLayout(button_layout)
# #         self.save_btn.clicked.connect(self.accept)
# #         self.cancel_btn.clicked.connect(self.reject)
# #         if self.path:
# #             self._populate_fields()

# #     def _populate_fields(self):
# #         index = self.dest_combo.findData(
# #             self.path.destination_id
# #         )
# #         if index >= 0:
# #             self.dest_combo.setCurrentIndex(index)
# #         self.distance_spin.setValue(self.path.distance_km)
# #         self.desc_edit.setText(self.path.description or "")

# #     def get_data(self):
# #         return {
# #             "origin": self.origin,
# #             "destination": self.dest_combo.currentData(),
# #             "distance_km": self.distance_spin.value(),
# #             "description": self.desc_edit.text(),
# #         }

# from PyQt6.QtWidgets import (
#     QDialog,
#     QLabel,
#     QLineEdit,
#     QSpinBox,
#     QComboBox,
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
# from db.models.world import Locality, Junction
# # from ui.dialogs.junction_editor import

# # Not yet written -- see the "expected JunctionEditorDialog interface"
# # note above _add_junction(). Adjust the import path once that file
# # exists.
# #
# # Expected interface:
# #   JunctionEditorDialog(repo, path: Path, junction: Junction = None, parent=None)
# #   .get_data() -> {
# #       "path_a": Path, "position_a_m": int,
# #       "path_b": Path, "position_b_m": int,
# #       "description": str,
# #   }
# # where path_a defaults to the current path when creating a new junction.
# # from ui.junction_editor import JunctionEditorDialog


# class PathEditorDialog(QDialog):
#     def __init__(
#         self, repo, origin: Locality, path=None, parent=None
#     ):
#         super().__init__(parent)
#         self.repo = repo
#         self.origin = origin
#         self.path = path
#         self._junctions: list[Junction] = []
#         self.setWindowTitle(
#             "Edit Path" if self.path else "Add Path"
#         )
#         self.setModal(True)
#         self.resize(480, 620)
#         self.base_layout = QVBoxLayout()
#         self.setLayout(self.base_layout)

#         self.dest_label = QLabel("Destination:")
#         self.base_layout.addWidget(self.dest_label)
#         self.dest_combo = QComboBox()
#         self.localities = self.repo.get_all_localities()
#         for loc in self.localities:
#             if loc != self.origin:
#                 self.dest_combo.addItem(loc.name, loc)
#         self.base_layout.addWidget(self.dest_combo)

#         self.origin_site_label = QLabel(
#             "Origin site (where this path leaves from):"
#         )
#         self.base_layout.addWidget(self.origin_site_label)
#         self.origin_site_combo = QComboBox()
#         for site in self.origin.sites:
#             self.origin_site_combo.addItem(site.name, site)
#         self.base_layout.addWidget(self.origin_site_combo)

#         self.dest_site_label = QLabel(
#             "Destination site (where this path arrives at):"
#         )
#         self.base_layout.addWidget(self.dest_site_label)
#         self.dest_site_combo = QComboBox()
#         self.base_layout.addWidget(self.dest_site_combo)
#         self.dest_combo.currentIndexChanged.connect(
#             self._reload_destination_sites
#         )

#         self.distance_label = QLabel("Distance (m):")
#         self.base_layout.addWidget(self.distance_label)
#         self.distance_spin = QSpinBox()
#         # Upper bound is a placeholder (500 km) -- raise it if your world
#         # has longer paths than that.
#         self.distance_spin.setRange(0, 500_000)
#         self.distance_spin.setValue(1000)
#         self.base_layout.addWidget(self.distance_spin)

#         self.desc_label = QLabel("Description:")
#         self.base_layout.addWidget(self.desc_label)
#         self.desc_edit = QLineEdit()
#         self.base_layout.addWidget(self.desc_edit)

#         self.base_layout.addWidget(self._build_junctions_group())

#         button_layout = QHBoxLayout()
#         self.save_btn = QPushButton("Save")
#         self.cancel_btn = QPushButton("Cancel")
#         button_layout.addWidget(self.save_btn)
#         button_layout.addWidget(self.cancel_btn)
#         self.base_layout.addLayout(button_layout)
#         self.save_btn.clicked.connect(self._validate_and_accept)
#         self.cancel_btn.clicked.connect(self.reject)

#         # Populate dest_site_combo for whatever destination is selected
#         # by default -- the signal connection above only fires on
#         # *changes*, so the initial state needs an explicit call.
#         self._reload_destination_sites()

#         if self.path:
#             self._populate_fields()

#     # ------------------------------------------------------------------
#     # Destination / site selection
#     # ------------------------------------------------------------------

#     def _reload_destination_sites(self):
#         self.dest_site_combo.clear()
#         destination = self.dest_combo.currentData()
#         if destination is None:
#             return
#         for site in destination.sites:
#             self.dest_site_combo.addItem(site.name, site)

#     def _validate_and_accept(self):
#         if self.origin_site_combo.currentData() is None:
#             QMessageBox.warning(
#                 self,
#                 "Missing Origin Site",
#                 f"{self.origin.name} has no sites defined yet. "
#                 "Add one before creating a path from it.",
#             )
#             return
#         if self.dest_site_combo.currentData() is None:
#             destination = self.dest_combo.currentData()
#             name = destination.name if destination else "The destination"
#             QMessageBox.warning(
#                 self,
#                 "Missing Destination Site",
#                 f"{name} has no sites defined yet. "
#                 "Add one before creating a path to it.",
#             )
#             return
#         self.accept()

#     # ------------------------------------------------------------------
#     # Junctions
#     # ------------------------------------------------------------------

#     def _build_junctions_group(self) -> QGroupBox:
#         group = QGroupBox("Junctions")
#         group_layout = QVBoxLayout()
#         group.setLayout(group_layout)

#         self.junctions_table = QTableWidget(0, 4)
#         self.junctions_table.setHorizontalHeaderLabels(
#             [
#                 "Position (this path)",
#                 "Other path",
#                 "Position (other path)",
#                 "Description",
#             ]
#         )
#         self.junctions_table.horizontalHeader().setSectionResizeMode(
#             3, QHeaderView.ResizeMode.Stretch
#         )
#         self.junctions_table.setEditTriggers(
#             QAbstractItemView.EditTrigger.NoEditTriggers
#         )
#         self.junctions_table.setSelectionBehavior(
#             QAbstractItemView.SelectionBehavior.SelectRows
#         )
#         self.junctions_table.setSelectionMode(
#             QAbstractItemView.SelectionMode.SingleSelection
#         )
#         self.junctions_table.cellDoubleClicked.connect(
#             lambda *_: self._edit_selected_junction()
#         )
#         group_layout.addWidget(self.junctions_table)

#         btn_layout = QHBoxLayout()
#         self.add_junction_btn = QPushButton("Add Junction")
#         self.remove_junction_btn = QPushButton("Remove Junction")
#         btn_layout.addWidget(self.add_junction_btn)
#         btn_layout.addWidget(self.remove_junction_btn)
#         group_layout.addLayout(btn_layout)
#         self.add_junction_btn.clicked.connect(self._add_junction)
#         self.remove_junction_btn.clicked.connect(
#             self._remove_selected_junction
#         )

#         # A new path has no id yet, so junctions (which FK to it) can't
#         # be created until the path itself is saved once.
#         if self.path is None:
#             group.setEnabled(False)
#             group.setToolTip(
#                 "Save the path first to add junctions."
#             )

#         self._reload_junctions_table()
#         return group

#     def _reload_junctions_table(self):
#         self.junctions_table.setRowCount(0)
#         if self.path is None:
#             return
#         self._junctions = list(self.path.junctions)
#         for junction in self._junctions:
#             other_path, other_position = junction.other_path(
#                 self.path
#             )
#             this_position = (
#                 junction.position_a_m
#                 if junction.path_a_id == self.path.id
#                 else junction.position_b_m
#             )
#             row = self.junctions_table.rowCount()
#             self.junctions_table.insertRow(row)
#             self.junctions_table.setItem(
#                 row, 0, QTableWidgetItem(f"{this_position} m")
#             )
#             self.junctions_table.setItem(
#                 row,
#                 1,
#                 QTableWidgetItem(
#                     f"{other_path.origin.name} -> {other_path.destination.name}"
#                 ),
#             )
#             self.junctions_table.setItem(
#                 row, 2, QTableWidgetItem(f"{other_position} m")
#             )
#             self.junctions_table.setItem(
#                 row,
#                 3,
#                 QTableWidgetItem(junction.description or ""),
#             )

#     def _add_junction(self):
#         # dialog = JunctionEditorDialog(
#         #     self.repo, path=self.path, parent=self
#         # )
#         # if dialog.exec():
#         #     data = dialog.get_data()
#         #     self.repo.add_junction(**data)
#         #     self._reload_junctions_table()
#         pass

#     def _edit_selected_junction(self):
#         # junction = self._selected_junction()
#         # if junction is None:
#         #     return
#         # dialog = JunctionEditorDialog(
#         #     self.repo,
#         #     path=self.path,
#         #     junction=junction,
#         #     parent=self,
#         # )
#         # if dialog.exec():
#         #     data = dialog.get_data()
#         #     self.repo.update_junction(junction.id, **data)
#         #     self._reload_junctions_table()
#         pass

#     def _remove_selected_junction(self):
#         junction = self._selected_junction()
#         if junction is None:
#             return
#         confirm = QMessageBox.question(
#             self,
#             "Remove Junction",
#             "Remove this junction? This cannot be undone.",
#             QMessageBox.StandardButton.Yes
#             | QMessageBox.StandardButton.No,
#         )
#         if confirm != QMessageBox.StandardButton.Yes:
#             return
#         self.repo.delete_junction(junction)
#         self._reload_junctions_table()

#     def _selected_junction(self) -> Junction | None:
#         row = self.junctions_table.currentRow()
#         if row < 0 or row >= len(self._junctions):
#             return None
#         return self._junctions[row]

#     # ------------------------------------------------------------------
#     # Path fields
#     # ------------------------------------------------------------------

#     def _populate_fields(self):
#         # NOTE: fixed vs. the original -- this used to compare
#         # self.path.destination_id (an int) against combo items storing
#         # Locality objects, which could never match.
#         index = self.dest_combo.findData(self.path.destination)
#         if index >= 0:
#             self.dest_combo.setCurrentIndex(index)
#             # ^ if this actually changes the index, currentIndexChanged
#             # fires _reload_destination_sites for us; if the default
#             # selection was already correct, it won't fire, but we
#             # already populated it once above, so either way
#             # dest_site_combo is correct by the time we get here.

#         origin_site = self.repo.get_site_by_id(
#             self.path.origin_site_id
#         )
#         o_index = self.origin_site_combo.findData(origin_site)
#         if o_index >= 0:
#             self.origin_site_combo.setCurrentIndex(o_index)

#         destination_site = self.repo.get_site_by_id(
#             self.path.destination_site_id
#         )
#         d_index = self.dest_site_combo.findData(destination_site)
#         if d_index >= 0:
#             self.dest_site_combo.setCurrentIndex(d_index)

#         self.distance_spin.setValue(self.path.distance_m)
#         self.desc_edit.setText(self.path.description or "")

#     def get_data(self):
#         return {
#             "origin": self.origin,
#             "destination": self.dest_combo.currentData(),
#             "origin_site": self.origin_site_combo.currentData(),
#             "destination_site": self.dest_site_combo.currentData(),
#             "distance_m": self.distance_spin.value(),
#             "description": self.desc_edit.text(),
#         }

from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QSpinBox,
    QComboBox,
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
from db.models.world import Locality, Junction

from ui.dialogs.junction_editor import JunctionEditorDialog


class PathEditorDialog(QDialog):
    def __init__(
        self, repo, origin: Locality, path=None, parent=None
    ):
        super().__init__(parent)
        self.repo = repo
        self.origin = origin
        self.path = path
        self._junctions: list[Junction] = []
        self.setWindowTitle(
            "Edit Path" if self.path else "Add Path"
        )
        self.setModal(True)
        self.resize(480, 620)
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

        self.origin_site_label = QLabel(
            "Origin site (where this path leaves from):"
        )
        self.layout.addWidget(self.origin_site_label)
        self.origin_site_combo = QComboBox()
        for site in self.origin.sites:
            self.origin_site_combo.addItem(site.name, site)
        self.layout.addWidget(self.origin_site_combo)

        self.dest_site_label = QLabel(
            "Destination site (where this path arrives at):"
        )
        self.layout.addWidget(self.dest_site_label)
        self.dest_site_combo = QComboBox()
        self.layout.addWidget(self.dest_site_combo)
        self.dest_combo.currentIndexChanged.connect(
            self._reload_destination_sites
        )

        self.length_label = QLabel("Length (m):")
        self.layout.addWidget(self.length_label)
        self.length_spin = QSpinBox()
        # Upper bound is a placeholder (500 km) -- raise it if your world
        # has longer paths than that.
        self.length_spin.setRange(0, 500_000)
        self.length_spin.setValue(1000)
        self.layout.addWidget(self.length_spin)

        self.desc_label = QLabel("Description:")
        self.layout.addWidget(self.desc_label)
        self.desc_edit = QLineEdit()
        self.layout.addWidget(self.desc_edit)

        self.junctions_group = self._build_junctions_group()
        self.layout.addWidget(self.junctions_group)

        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.close_btn = QPushButton("Close")
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.close_btn)
        self.layout.addLayout(button_layout)
        # Save persists immediately but does NOT close the dialog -- a new
        # path has to exist in the DB before junctions (which FK to it)
        # can be added. "Close" is the only button that ends the dialog
        # now. Whatever code opens this dialog should stop calling
        # repo.add_path/update_path after exec() returns -- that now
        # happens inside the dialog itself, on each Save click.
        self.save_btn.clicked.connect(self._save)
        self.close_btn.clicked.connect(self.reject)

        # Populate dest_site_combo for whatever destination is selected
        # by default -- the signal connection above only fires on
        # *changes*, so the initial state needs an explicit call.
        self._reload_destination_sites()

        if self.path:
            self._populate_fields()

    # ------------------------------------------------------------------
    # Destination / site selection
    # ------------------------------------------------------------------

    def _reload_destination_sites(self):
        self.dest_site_combo.clear()
        destination = self.dest_combo.currentData()
        if destination is None:
            return
        for site in destination.sites:
            self.dest_site_combo.addItem(site.name, site)

    def _validate(self) -> bool:
        if self.origin_site_combo.currentData() is None:
            QMessageBox.warning(
                self,
                "Missing Origin Site",
                f"{self.origin.name} has no sites defined yet. "
                "Add one before creating a path from it.",
            )
            return False
        if self.dest_site_combo.currentData() is None:
            destination = self.dest_combo.currentData()
            name = (
                destination.name
                if destination
                else "The destination"
            )
            QMessageBox.warning(
                self,
                "Missing Destination Site",
                f"{name} has no sites defined yet. "
                "Add one before creating a path to it.",
            )
            return False
        return True

    # ------------------------------------------------------------------
    # Junctions
    # ------------------------------------------------------------------

    def _build_junctions_group(self) -> QGroupBox:
        group = QGroupBox("Junctions")
        group_layout = QVBoxLayout()
        group.setLayout(group_layout)

        self.junctions_table = QTableWidget(0, 4)
        self.junctions_table.setHorizontalHeaderLabels(
            [
                "Position (this path)",
                "Other path",
                "Position (other path)",
                "Description",
            ]
        )
        self.junctions_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.Stretch
        )
        self.junctions_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.junctions_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.junctions_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.junctions_table.cellDoubleClicked.connect(
            lambda *_: self._edit_selected_junction()
        )
        group_layout.addWidget(self.junctions_table)

        btn_layout = QHBoxLayout()
        self.add_junction_btn = QPushButton("Add Junction")
        self.remove_junction_btn = QPushButton(
            "Remove Junction"
        )
        btn_layout.addWidget(self.add_junction_btn)
        btn_layout.addWidget(self.remove_junction_btn)
        group_layout.addLayout(btn_layout)
        self.add_junction_btn.clicked.connect(
            self._add_junction
        )
        self.remove_junction_btn.clicked.connect(
            self._remove_selected_junction
        )

        # A new path has no id yet, so junctions (which FK to it) can't
        # be created until the path itself is saved once.
        if self.path is None:
            group.setEnabled(False)
            group.setToolTip(
                "Save the path first to add junctions."
            )

        self._reload_junctions_table()
        return group

    def _reload_junctions_table(self):
        self.junctions_table.setRowCount(0)
        if self.path is None:
            return
        self._junctions = list(self.path.junctions)
        for junction in self._junctions:
            other_path, other_position = (
                junction.other_path(self.path)
            )
            this_position = (
                junction.position_a_m
                if junction.path_a_id == self.path.id
                else junction.position_b_m
            )
            row = self.junctions_table.rowCount()
            self.junctions_table.insertRow(row)
            self.junctions_table.setItem(
                row,
                0,
                QTableWidgetItem(f"{this_position} m"),
            )
            self.junctions_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    f"{other_path.origin.name} -> {other_path.destination.name}"
                ),
            )
            self.junctions_table.setItem(
                row,
                2,
                QTableWidgetItem(f"{other_position} m"),
            )
            self.junctions_table.setItem(
                row,
                3,
                QTableWidgetItem(
                    junction.description or ""
                ),
            )

    def _add_junction(self):
        dialog = JunctionEditorDialog(
            self.repo, path=self.path, parent=self
        )
        if dialog.exec():
            data = dialog.get_data()
            self.repo.add_junction(**data)
            self._reload_junctions_table()

    def _edit_selected_junction(self):
        junction = self._selected_junction()
        if junction is None:
            return
        dialog = JunctionEditorDialog(
            self.repo,
            path=self.path,
            junction=junction,
            parent=self,
        )
        if dialog.exec():
            data = dialog.get_data()
            self.repo.update_junction(junction.id, **data)
            self._reload_junctions_table()

    def _remove_selected_junction(self):
        junction = self._selected_junction()
        if junction is None:
            return
        confirm = QMessageBox.question(
            self,
            "Remove Junction",
            "Remove this junction? This cannot be undone.",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        self.repo.delete_junction(junction)
        self._reload_junctions_table()

    def _selected_junction(self) -> Junction | None:
        row = self.junctions_table.currentRow()
        if row < 0 or row >= len(self._junctions):
            return None
        return self._junctions[row]

    # ------------------------------------------------------------------
    # Path fields
    # ------------------------------------------------------------------

    def _populate_fields(self):
        # NOTE: fixed vs. the original -- this used to compare
        # self.path.destination_id (an int) against combo items storing
        # Locality objects, which could never match.
        index = self.dest_combo.findData(
            self.path.destination
        )
        if index >= 0:
            self.dest_combo.setCurrentIndex(index)
            # ^ if this actually changes the index, currentIndexChanged
            # fires _reload_destination_sites for us; if the default
            # selection was already correct, it won't fire, but we
            # already populated it once above, so either way
            # dest_site_combo is correct by the time we get here.

        origin_site = self.repo.get_site_by_id(
            self.path.origin_site_id
        )
        o_index = self.origin_site_combo.findData(
            origin_site
        )
        if o_index >= 0:
            self.origin_site_combo.setCurrentIndex(o_index)

        destination_site = self.repo.get_site_by_id(
            self.path.destination_site_id
        )
        d_index = self.dest_site_combo.findData(
            destination_site
        )
        if d_index >= 0:
            self.dest_site_combo.setCurrentIndex(d_index)

        self.length_spin.setValue(self.path.length_m)
        self.desc_edit.setText(self.path.description or "")

    def get_data(self):
        return {
            "origin": self.origin,
            "destination": self.dest_combo.currentData(),
            "origin_site": self.origin_site_combo.currentData(),
            "destination_site": self.dest_site_combo.currentData(),
            "length_m": self.length_spin.value(),
            "description": self.desc_edit.text(),
        }

    def _save(self):
        if not self._validate():
            return
        data = self.get_data()
        if self.path is None:
            self.path = self.repo.add_path(**data)
            self.junctions_group.setEnabled(True)
            self.junctions_group.setToolTip("")
            self._reload_junctions_table()
        else:
            self.repo.update_path(self.path.id, **data)
        self.setWindowTitle(
            f"Edit Path — {self.origin.name} -> {self.path.destination.name}"
        )
