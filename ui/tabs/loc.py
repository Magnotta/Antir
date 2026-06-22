from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QHeaderView,
)
from PyQt6.QtCore import Qt
from db.repository.location import LocationRepository
from core.game_state import GameState
from ..dialogs.locality_editor import LocalityEditorDialog
from ..dialogs.path_condition_editor import (
    ConditionEditorDialog,
)
from ..dialogs.path_editor import PathEditorDialog


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
