import sys
from PyQt6.QtWidgets import (
    QApplication,
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
    QStackedWidget,
    QSpinBox,
    QFormLayout,
)
from PyQt6.QtCore import Qt
from db.models import Locality, Path, PointCondition, SegmentCondition
from core.defs import PATH_CONDITION_KINDS


class ConditionEditorDialog(QDialog):
    def __init__(self, path_id: int, condition=None, parent=None):
        super().__init__(parent)
        self.path_id = path_id
        self.condition = condition
        self.setWindowTitle(
            "Edit Condition" if self.condition else "Add Condition"
        )
        self.setModal(True)
        self.resize(420, 350)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("Condition Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(PATH_CONDITION_KINDS.keys())
        self.layout.addWidget(self.type_combo)
        self.layout.addWidget(QLabel("Key:"))
        self.key_edit = QLineEdit()
        self.layout.addWidget(self.key_edit)
        self.form = QFormLayout()
        # self.layout.addWidget(QLabel("Value:"))
        # self.value_stack = QStackedWidget()
        # self.int_value = QSpinBox()
        # self.int_value.setRange(-999999, 999999)
        # self.value_stack.addWidget(self.int_value)
        # self.text_value = QLineEdit()
        # self.value_stack.addWidget(self.text_value)
        self.layout.addWidget(self.value_stack)
        self.layout.addWidget(QLabel("Description (optional):"))
        self.desc_edit = QTextEdit()
        self.layout.addWidget(self.desc_edit)
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(btn_layout)
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.type_combo.currentTextChanged.connect(
            self._update_value_widget
        )
        if self.condition:
            self._populate_fields()
        self._update_value_widget()

    def _update_value_widget(self):
        condition_type = self.type_combo.currentText()
        if condition_type in ["level", "skill"]:
            self.value_stack.setCurrentWidget(self.int_value)
        else:
            self.value_stack.setCurrentWidget(self.text_value)

    def _populate_fields(self):
        self.type_combo.setCurrentText(self.condition.condition_type)
        self.key_edit.setText(self.condition.key)
        self.operator_combo.setCurrentText(self.condition.operator)
        self.desc_edit.setText(self.condition.description or "")
        if self.condition.condition_type in ["level", "skill"]:
            try:
                self.int_value.setValue(int(self.condition.value))
            except:
                self.int_value.setValue(0)
        else:
            self.text_value.setText(self.condition.value or "")

    def get_data(self):
        condition_type = self.type_combo.currentText()
        if condition_type in ["level", "skill"]:
            value = str(self.int_value.value())
        else:
            value = self.text_value.text().strip()
        return {
            "path_id": self.path_id,
            "condition_type": condition_type,
            "key": self.key_edit.text().strip(),
            "operator": self.operator_combo.currentText(),
            "value": value,
            "description": self.desc_edit.toPlainText().strip(),
        }


class PathEditorDialog(QDialog):
    def __init__(self, repo, origin: Locality, path=None, parent=None):
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
        index = self.dest_combo.findData(self.path.destination_id)
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
            "Edit Locality" if self.locality else "New Locality"
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
        self.desc_edit.setText(self.locality.description or "")

    def get_data(self):
        return {
            "name": self.name_edit.text().strip(),
            "tags": self.tags_edit.text().strip(),
            "description": self.desc_edit.toPlainText().strip(),
        }


class LocalityTab(QWidget):
    def __init__(self, repo, state):
        super().__init__()
        self.repo = repo
        self.game_state = state
        self.setWindowTitle("Locality Viewer")
        self.resize(800, 500)
        self.locality_label = QLabel()
        self.locality_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        path_label = QLabel("Paths")
        path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paths_table = QTableWidget()
        self.paths_table.setColumnCount(4)
        self.paths_table.setHorizontalHeaderLabels(
            ["ID", "Destination", "Distance (km)", "Description"]
        )
        self.paths_table.itemDoubleClicked.connect(self.edit_selected_path)
        self.paths_table.selectionModel().selectionChanged.connect(
            self.on_path_selected
        )
        header = self.paths_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        left = QVBoxLayout()
        left.addWidget(path_label)
        left.addWidget(self.paths_table)
        conditions_label = QLabel("Path Conditions")
        conditions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.conditions_table = QTableWidget()
        self.conditions_table.setColumnCount(3)
        self.conditions_table.setHorizontalHeaderLabels(
            ["Kind", "Position", "Value"]
        )
        header = self.conditions_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        right = QVBoxLayout()
        right.addWidget(conditions_label)
        right.addWidget(self.conditions_table)
        tables_layout = QHBoxLayout()
        tables_layout.addLayout(left)
        tables_layout.addLayout(right)
        self.add_path_btn = QPushButton("New Path")
        self.add_path_btn.clicked.connect(self.add_path)
        self.add_point_btn = QPushButton("Add Point Cond")
        self.add_point_btn.setEnabled(False)
        self.add_point_btn.clicked.connect(self.add_point_condition)
        self.add_segment_btn = QPushButton("Add Segm Cond")
        self.add_segment_btn.setEnabled(False)
        self.add_segment_btn.clicked.connect(self.add_segment_condition)
        self.new_locality_btn = QPushButton("New Locality")
        self.new_locality_btn.clicked.connect(self.create_locality)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.new_locality_btn)
        button_layout.addWidget(self.add_path_btn)
        button_layout.addWidget(self.add_point_btn)
        button_layout.addWidget(self.add_segment_btn)
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(tables_layout)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.locality_label)
        self.refresh()

    def on_path_selected(self):
        has_selection = bool(self.get_selected_path())
        self.add_point_btn.setEnabled(has_selection)
        self.add_segment_btn.setEnabled(has_selection)

    def get_selected_path(self):
        selected = self.paths_table.selectedItems()
        if not selected:
            return None
        row = selected[0].row()
        path_id = int(self.paths_table.item(row, 0).text())
        return self.repo.get_path_by_id(path_id)

    def create_locality(self):
        dialog = LocalityEditorDialog(self.repo, parent=self)
        if dialog.exec():
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(self, "Error", "Name cannot be empty.")
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
            parent=self
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
        self.locality_label.setText(
            f"Current Locality: {self.game_state.locality.name}"
        )
        paths = self.repo.get_paths_from(self.game_state.locality)
        self.paths_table.setRowCount(len(paths))
        for row, path in enumerate(paths):
            self.paths_table.setItem(row, 0, QTableWidgetItem(str(path.id)))
            self.paths_table.setItem(row, 1, QTableWidgetItem(path.destination.name))
            self.paths_table.setItem(
                row, 2, QTableWidgetItem(str(path.distance_km))
            )
            self.paths_table.setItem(
                row, 3, QTableWidgetItem(path.description or "")
            )
        self.paths_table.resizeColumnsToContents()
        self.conditions_table.setRowCount(0)

    def refresh_conditions_table(self):
        selected_row = self.paths_table.currentRow()
        if selected_row < 0:
            self.conditions_table.setRowCount(0)
            return
        paths = self.repo.get_paths_from(self.locality_id)
        path = paths[selected_row]
        point_conditions = path.point_conditions
        segment_conditions = path.segment_conditions
        total = len(point_conditions) + len(segment_conditions)
        self.conditions_table.setRowCount(total)
        row = 0
        for cond in point_conditions:
            self.conditions_table.setItem(
                row, 0, QTableWidgetItem("Point")
            )
            self.conditions_table.setItem(
                row, 1, QTableWidgetItem(cond.kind)
            )
            self.conditions_table.setItem(
                row, 2, QTableWidgetItem(str(cond.position))
            )
            self.conditions_table.setItem(
                row, 3, QTableWidgetItem(cond.value)
            )
            row += 1
        for cond in segment_conditions:
            self.conditions_table.setItem(
                row, 0, QTableWidgetItem("Segment")
            )
            self.conditions_table.setItem(
                row, 1, QTableWidgetItem(cond.kind)
            )
            self.conditions_table.setItem(
                row, 2, QTableWidgetItem(f"{str(cond.start)}-{str(cond.end)}")
            )
            self.conditions_table.setItem(
                row, 3, QTableWidgetItem(cond.value)
            )
            row += 1

        self.conditions_table.resizeColumnsToContents()

    def add_path(self):
        dialog = PathEditorDialog(self.repo, self.game_state.locality, parent=self)
        if dialog.exec():
            data = dialog.get_data()
            self.repo.add_path(
                data["origin"],
                data["destination"],
                distance_km=data["distance_km"],
                description=data["description"],
            )
            self.refresh()

    def add_point_condition(self):
        path = self.get_selected_path()
        if not path:
            return
        dialog = ConditionEditorDialog(path.id, parent=self)
        if dialog.exec():
            data = dialog.get_data()
            self.repo.add_condition(**data)
            self.refresh_conditions()

    def add_segment_condition(self):
        path = self.get_selected_path()
        if not path:
            return
        self.repo.add_segment_condition(
            path.id,
            start=0.2,
            end=0.8,
            kind="terrain",
            value="forest",
        )
        QMessageBox.information(self, "Success", "Segment condition added.")
