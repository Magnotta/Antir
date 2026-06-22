from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTableView,
    QPushButton,
    QMessageBox,
    QHeaderView,
)
from PyQt6.QtCore import (
    QModelIndex,
)
from db.models.item import Item
from db.repository.item import ItemRepository
from ..models.item_table import ItemTableModel
from ..models.mold_table import MoldTableModel
from ..dialogs.slot_editor import OccupiedSlotsEditorDialog
from ..dialogs.spawn_item import SpawnItemDialog
from ..dialogs.mold_editor import MoldEditor
from ..dialogs.item_editor import ItemEditorDialog


class ItemTab(QWidget):
    def __init__(
        self,
        item_repo: ItemRepository,
        parent=None,
    ):
        super().__init__(parent)
        self.item_repo = item_repo
        self.search_mold = QLineEdit()
        self.search_mold.setPlaceholderText("Search molds…")
        self.search_mold.textChanged.connect(
            self.on_search_mold
        )
        self.mold_table_model = MoldTableModel()
        self.mold_table = QTableView()
        self.mold_table.setModel(self.mold_table_model)
        header = self.mold_table.horizontalHeader()
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
        self.mold_table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )
        self.mold_table.setSelectionMode(
            QTableView.SelectionMode.SingleSelection
        )
        (
            self.mold_table.selectionModel().selectionChanged.connect(
                self.on_mold_selected
            )
        )
        self.mold_table.doubleClicked.connect(
            self.on_mold_double_clicked
        )
        self.add_mold_btn = QPushButton("Add")
        self.add_mold_btn.clicked.connect(self.add_mold)
        self.edit_mold_btn = QPushButton("Edit")
        self.edit_mold_btn.clicked.connect(self.edit_mold)
        self.edit_mold_btn.setEnabled(False)
        self.del_mold_btn = QPushButton("Delete")
        self.del_mold_btn.clicked.connect(self.delete_mold)
        self.del_mold_btn.setEnabled(False)
        self.edit_slots_btn = QPushButton("Slots")
        self.edit_slots_btn.clicked.connect(
            self.on_edit_occupied_slots
        )
        left_btn_layout = QHBoxLayout()
        left_btn_layout.addWidget(self.add_mold_btn)
        left_btn_layout.addWidget(self.edit_mold_btn)
        left_btn_layout.addWidget(self.del_mold_btn)
        left_btn_layout.addWidget(self.edit_slots_btn)
        left = QVBoxLayout()
        left.addWidget(self.search_mold)
        left.addWidget(self.mold_table)
        left.addLayout(left_btn_layout)
        right = QVBoxLayout()
        self.search_item = QLineEdit()
        self.search_item.setPlaceholderText("Search items…")
        self.search_item.textChanged.connect(
            self.on_search_item
        )
        self.item_table = QTableView()
        self.item_table_model = ItemTableModel()
        self.item_table.setModel(self.item_table_model)
        header = self.item_table.horizontalHeader()
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
        self.item_table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )
        self.item_table.setSelectionMode(
            QTableView.SelectionMode.SingleSelection
        )
        (
            self.item_table.selectionModel().selectionChanged.connect(
                self.on_item_selected
            )
        )
        self.item_table.doubleClicked.connect(
            self.on_item_double_clicked
        )
        self.spawn_item_btn = QPushButton("SPAWN")
        self.spawn_item_btn.setEnabled(False)
        self.spawn_item_btn.clicked.connect(self.spawn_item)
        self.edit_item_btn = QPushButton("EDIT ITEM")
        self.edit_item_btn.clicked.connect(
            self.on_edit_clicked
        )
        self.edit_item_btn.setEnabled(False)
        self.item_table.selectionModel().selectionChanged.connect(
            lambda *_: self.edit_item_btn.setEnabled(
                bool(
                    self.item_table.selectionModel().selectedRows()
                )
            )
        )
        self.destroy_item_btn = QPushButton("DESTROY")
        self.destroy_item_btn.setEnabled(False)
        self.destroy_item_btn.clicked.connect(
            self.destroy_item
        )
        right_btn_layout = QHBoxLayout()
        right_btn_layout.addWidget(self.spawn_item_btn)
        right_btn_layout.addWidget(self.edit_item_btn)
        right_btn_layout.addWidget(self.destroy_item_btn)
        right.addWidget(self.search_item)
        right.addWidget(self.item_table)
        right.addLayout(right_btn_layout)
        layout = QHBoxLayout()
        layout.addLayout(left, 1)
        layout.addLayout(right, 1)
        self.setLayout(layout)
        self.refresh_items()
        self.refresh_molds()

    def on_edit_occupied_slots(self):
        index = (
            self.mold_table.selectionModel().selectedRows()[
                0
            ]
        )
        mold = self.mold_table_model.molds[index.row()]
        if not mold:
            QMessageBox.warning(
                self, "No selection", "Select a mold first."
            )
            return
        dlg = OccupiedSlotsEditorDialog(
            mold, self.item_repo, self
        )
        if dlg.exec():
            self.item_repo.session.commit()

    def refresh_molds(self, search: str | None = None):
        molds = self.item_repo.get_all_molds(search=search)
        self.mold_table_model = MoldTableModel(molds)
        self.mold_table.setModel(self.mold_table_model)
        (
            self.mold_table.selectionModel().selectionChanged.connect(
                self.on_mold_selected
            )
        )
        self.mold_table.setColumnWidth(0, 5)

    def refresh_items(self, search: str | None = None):
        items = self.item_repo.get_extant_items(
            search=search
        )
        self.item_table_model = ItemTableModel(items)
        self.item_table.setModel(self.item_table_model)
        (
            self.item_table.selectionModel().selectionChanged.connect(
                self.on_item_selected
            )
        )
        self.item_table.setColumnWidth(0, 5)

    def _get_selected_item(self) -> Item | None:
        selection = (
            self.item_table.selectionModel().selectedRows()
        )
        if not selection:
            return None

        row = selection[0].row()
        return self.item_table_model.items[row]

    def on_edit_clicked(self):
        item = self._get_selected_item()
        if not item:
            QMessageBox.warning(
                self,
                "No selection",
                "Select an item to edit.",
            )
            return
        self.edit_item(item)

    def on_item_double_clicked(self, index: QModelIndex):
        item = self.item_table_model.items[index.row()]
        self.edit_item(item)

    def spawn_item(self):
        index = (
            self.mold_table.selectionModel().selectedRows()[
                0
            ]
        )
        mold = self.mold_table_model.molds[index.row()]
        dlg = SpawnItemDialog(self.item_repo, mold, self)
        if dlg.exec():
            manual_params = dlg.get_manual_params()
            self.item_repo.spawn(
                mold,
                666,
                manual_params,
            )
            self.refresh_items()

    def destroy_item(self):
        index = (
            self.item_table.selectionModel().selectedRows()[
                0
            ]
        )
        item = self.item_table_model.items[index.row()]
        confirm = QMessageBox.question(
            self,
            "Destroy Item",
            f"Destroy item with ID {item.id}?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        self.item_repo.destroy_item(item)
        self.refresh_items()

    def edit_item(self, item: Item):
        dlg = ItemEditorDialog(
            item, self.item_repo, parent=self
        )
        if dlg.exec():
            self.refresh_items()

    def on_search_mold(self, text: str):
        self.refresh_molds(search=text)

    def on_search_item(self, text: str):
        self.refresh_items(search=text)

    def delete_mold(self):
        indexes = (
            self.mold_table.selectionModel().selectedRows()
        )
        if not indexes:
            return
        item = self.mold_table_model.molds[indexes[0].row()]
        if not self.confirm_delete(
            "Delete Item Mold",
            "Are you sure you want to delete"
            f"'{item.name}'?\n\n"
            "This action cannot be undone.",
        ):
            return
        self.item_repo.delete_mold(item)
        self.refresh_molds()

    def add_mold(self):
        dlg = MoldEditor(self.item_repo, parent=self)
        if dlg.exec():
            self.refresh_molds()

    def on_mold_double_clicked(self, index: QModelIndex):
        if not index.isValid():
            return
        row = index.row()
        mold = self.mold_table_model.molds[row]
        dlg = MoldEditor(self.item_repo, mold=mold)
        if dlg.exec():
            self.refresh_molds()

    def edit_mold(self):
        indexes = (
            self.mold_table.selectionModel().selectedRows()
        )
        if not indexes:
            return
        mold = self.mold_table_model.molds[indexes[0].row()]
        dlg = MoldEditor(
            self.item_repo,
            mold,
            parent=self,
        )
        if dlg.exec():
            self.refresh_molds()

    def confirm_delete(
        self, title: str, message: str
    ) -> bool:
        reply = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        return reply == QMessageBox.StandardButton.Yes

    def on_mold_selected(self):
        has_selection = bool(
            self.mold_table.selectionModel().selectedRows()
        )
        self.spawn_item_btn.setEnabled(has_selection)
        self.edit_mold_btn.setEnabled(has_selection)
        self.del_mold_btn.setEnabled(has_selection)

    def on_item_selected(self):
        has_selection = bool(
            self.item_table.selectionModel().selectedRows()
        )
        self.edit_item_btn.setEnabled(has_selection)
        self.destroy_item_btn.setEnabled(has_selection)
