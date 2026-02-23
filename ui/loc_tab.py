from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QDoubleSpinBox,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QHeaderView,
    QSpinBox,
    QFormLayout,
)
from PyQt6.QtCore import Qt
from db.models import (
    Locality,
    PointCondition,
    SegmentCondition,
)
from db.repository import LocationRepository
from core.defs import (
    PATH_CONDITION_KINDS,
    STR_PATH_COND_PARAMS,
    SEGM_COND_KINDS,
)
from core.game_state import GameState


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


class LocalityTab(QWidget):
    def __init__(
        self, repo: LocationRepository, state: GameState
    ):
        super().__init__()
        self.repo = repo
        self.game_state = state
        self.setWindowTitle("Locality Viewer")
        self.resize(800, 500)
        self.locality_label = QLabel()
        self.locality_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        path_label = QLabel("Paths")
        path_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.paths_table = QTableWidget()
        self.paths_table.setColumnCount(4)
        self.paths_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Destination",
                "Distance (km)",
                "Description",
            ]
        )
        self.paths_table.itemDoubleClicked.connect(
            self.edit_selected_path
        )
        self.paths_table.selectionModel().selectionChanged.connect(
            self.on_path_selected
        )
        header = self.paths_table.horizontalHeader()
        header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            3, QHeaderView.ResizeMode.Stretch
        )
        left = QVBoxLayout()
        left.addWidget(path_label)
        left.addWidget(self.paths_table)
        conditions_label = QLabel("Path Conditions")
        conditions_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.conditions_table = QTableWidget()
        self.conditions_table.setColumnCount(5)
        self.conditions_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Kind",
                "Norm Pos",
                "Data",
                "Description",
            ]
        )
        header = self.conditions_table.horizontalHeader()
        self.conditions_table.doubleClicked.connect(
            self._edit_condition_from_index
        )
        header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            4, QHeaderView.ResizeMode.Stretch
        )
        right = QVBoxLayout()
        right.addWidget(conditions_label)
        right.addWidget(self.conditions_table)
        tables_layout = QHBoxLayout()
        tables_layout.addLayout(left)
        tables_layout.addLayout(right)
        self.add_path_btn = QPushButton("New Path")
        self.add_path_btn.clicked.connect(self.add_path)
        self.new_locality_btn = QPushButton("New Locality")
        self.new_locality_btn.clicked.connect(
            self.create_locality
        )
        self.add_cond_btn = QPushButton("Add Condition")
        self.add_cond_btn.clicked.connect(
            self.add_condition
        )
        self.add_cond_btn.setEnabled(False)
        self.del_cond_btn = QPushButton("Del Condition")
        self.del_cond_btn.clicked.connect(
            self.delete_selected_condition
        )
        self.del_cond_btn.setEnabled(False)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.new_locality_btn)
        button_layout.addWidget(self.add_path_btn)
        button_layout.addWidget(self.add_cond_btn)
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(tables_layout)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.locality_label)
        self.refresh()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.delete_selected_condition()
        else:
            super().keyPressEvent(event)

    def on_path_selected(self):
        has_selection = bool(self.get_selected_path())
        self.add_cond_btn.setEnabled(has_selection)
        self.del_cond_btn.setEnabled(has_selection)
        self.refresh_conditions_table()

    def get_selected_path(self):
        selected = self.paths_table.selectedItems()
        if not selected:
            return None
        row = selected[0].row()
        path_id = int(self.paths_table.item(row, 0).text())
        return self.repo.get_path_by_id(path_id)

    def create_locality(self):
        dialog = LocalityEditorDialog(
            self.repo, parent=self
        )
        if dialog.exec():
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(
                    self, "Error", "Name cannot be empty."
                )
                return
            locality = self.repo.add_locality(
                name=data["name"],
                description=data["description"],
                data=None,
            )
            self.locality_id = locality.id
            self.refresh()

    def edit_selected_path(self):
        path = self.get_selected_path()
        if not path:
            return
        dialog = PathEditorDialog(
            self.repo,
            self.game_state.locality,
            path=path,
            parent=self,
        )
        if dialog.exec():
            data = dialog.get_data()
            self.repo.update_path(
                path.id,
                destination_id=data["destination_id"],
                distance_km=data["distance_km"],
                description=data["description"],
            )
            self.refresh()

    def refresh(self):
        if self.game_state.locality is None:
            self.locality_label.setText(
                "Current Locality: None"
            )
            return
        self.locality_label.setText(
            f"Current Locality: {self.game_state.locality.name}"
        )
        paths = self.repo.get_paths_from(
            self.game_state.locality
        )
        self.paths_table.setRowCount(len(paths))
        for row, path in enumerate(paths):
            self.paths_table.setItem(
                row, 0, QTableWidgetItem(str(path.id))
            )
            self.paths_table.setItem(
                row,
                1,
                QTableWidgetItem(path.destination.name),
            )
            self.paths_table.setItem(
                row,
                2,
                QTableWidgetItem(str(path.distance_km)),
            )
            self.paths_table.setItem(
                row,
                3,
                QTableWidgetItem(path.description or ""),
            )
        self.paths_table.resizeColumnsToContents()
        self.conditions_table.setRowCount(0)

    def refresh_conditions_table(self):
        selected_row = self.paths_table.currentRow()
        if selected_row < 0:
            self.conditions_table.setRowCount(0)
            return
        paths = self.repo.get_paths_from(
            self.game_state.locality
        )
        path = paths[selected_row]
        point_conditions = path.point_conditions
        segment_conditions = path.segment_conditions
        total = len(point_conditions) + len(
            segment_conditions
        )
        self.conditions_table.setRowCount(total)
        row = 0
        for cond in point_conditions:
            self.conditions_table.setItem(
                row, 0, QTableWidgetItem(str(cond.id))
            )
            self.conditions_table.setItem(
                row, 1, QTableWidgetItem(cond.kind)
            )
            self.conditions_table.setItem(
                row, 2, QTableWidgetItem(str(cond.position))
            )
            self.conditions_table.setItem(
                row,
                3,
                QTableWidgetItem(
                    ", ".join(
                        "{}={}".format(k, v)
                        for k, v in cond.data.items()
                    )
                ),
            )
            self.conditions_table.setItem(
                row, 4, QTableWidgetItem(cond.description)
            )
            row += 1
        for cond in segment_conditions:
            self.conditions_table.setItem(
                row, 0, QTableWidgetItem(str(cond.id))
            )
            self.conditions_table.setItem(
                row, 1, QTableWidgetItem(cond.kind)
            )
            self.conditions_table.setItem(
                row,
                2,
                QTableWidgetItem(
                    f"{str(cond.start)}-{str(cond.end)}"
                ),
            )
            self.conditions_table.setItem(
                row,
                3,
                QTableWidgetItem(
                    ", ".join(
                        "{}={}".format(k, v)
                        for k, v in cond.data.items()
                    )
                ),
            )
            self.conditions_table.setItem(
                row, 4, QTableWidgetItem(cond.description)
            )
            row += 1
        self.conditions_table.resizeColumnsToContents()

    def add_path(self):
        dialog = PathEditorDialog(
            self.repo, self.game_state.locality, parent=self
        )
        if dialog.exec():
            data = dialog.get_data()
            self.repo.add_path(
                data["origin"],
                data["destination"],
                distance_km=data["distance_km"],
                description=data["description"],
            )
            self.refresh()

    def add_condition(self):
        path = self.get_selected_path()
        if not path:
            return
        dialog = ConditionEditorDialog(path.id, parent=self)
        if dialog.exec():
            data = dialog.get_data()
            if "position" in data.keys():
                self.repo.add_point_condition(**data)
            else:
                self.repo.add_segment_condition(**data)
            self.refresh_conditions_table()

    def get_selected_condition(self):
        selected = self.conditions_table.selectedItems()
        if not selected:
            return None
        row = selected[0].row()
        id_item = self.conditions_table.item(row, 0)
        if not id_item:
            return None
        condition_id = int(id_item.text())
        return self.repo.get_condition_by_id(condition_id)

    def _edit_condition_from_index(self, index):
        row = index.row()
        condition_id_item = self.conditions_table.item(
            row, 0
        )
        if not condition_id_item:
            return
        condition_id = int(condition_id_item.text())
        condition = self.repo.get_condition_by_id(
            condition_id
        )
        if not condition:
            return
        dialog = ConditionEditorDialog(
            path_id=condition.path_id,
            condition=condition,
            parent=self,
        )
        if dialog.exec():
            data = dialog.get_data()
            self.repo.update_condition(condition, **data)
            self.refresh_conditions_table()

    def delete_selected_condition(self):
        condition = self.get_selected_condition()
        if not condition:
            return
        reply = QMessageBox.critical(
            self,
            "Delete Condition",
            "You are about to permanently delete this condition:\n\n"
            "This action cannot be undone.\n\n"
            "Do you want to proceed?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.repo.delete_condition(condition)
            self.refresh_conditions_table()
