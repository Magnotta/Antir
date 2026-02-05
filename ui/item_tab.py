from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTableView,
    QPushButton,
    QDialog,
    QTextEdit,
    QMessageBox,
    QFormLayout,
    QCompleter,
    QListWidget,
)

from PyQt6.QtCore import (
    QAbstractTableModel,
    Qt,
    QTimer,
    QModelIndex,
    QSortFilterProxyModel,
    QStringListModel,
    pyqtSlot,
)
from db.models import ItemMold, Item
from db.repository import (
    ItemMoldRepository,
    ItemRepository,
)
from core.defs import ITEMMOLD_TAGS


class TagFilterModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )

    def set_filter_text(self, text: str):
        self.setFilterFixedString(text)

    def filterAcceptsRow(self, row, parent):
        if not self.filterRegularExpression().pattern():
            return True
        source = self.sourceModel().index(row, 0, parent)
        return (
            self.filterRegularExpression().pattern().lower()
            in source.data().lower()
        )


class ItemMoldTableModel(QAbstractTableModel):
    HEADERS = ["ID", "Name", "Tags", "Description"]

    def __init__(self, itemmolds: list[ItemMold] = []):
        super().__init__()
        self.itemmolds = itemmolds

    def rowCount(self, parent=QModelIndex()):
        return len(self.itemmolds)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        item = self.itemmolds[index.row()]
        col = index.column()
        return [
            item.id,
            item.name,
            item.tags,
            item.description,
        ][col]

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return section + 1

    def delete_row(self, row: int):
        item = self.itemmolds[row]
        self.session.delete(item)
        self.session.commit()
        self.refresh()


class ItemTableModel(QAbstractTableModel):
    HEADERS = ["ID", "Mold", "Owner", "Container"]

    def __init__(self, items: list[Item] = []):
        super().__init__()
        self.items = items

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        item = self.items[index.row()]
        col = index.column()
        if col == 0:
            return item.id
        if col == 1:
            return item.original_mold
        if col == 2:
            return item.owner
        if col == 3:
            return item.container_item_id

    def headerData(self, section, orientation, role):
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return self.HEADERS[section]
        return None


class ItemTab(QWidget):
    def __init__(
        self,
        itemmold_repo: ItemMoldRepository,
        item_repo: ItemRepository,
        parent=None,
    ):
        super().__init__(parent)
        self.itemmold_repo = itemmold_repo
        self.item_repo = item_repo
        self.search_itemmold = QLineEdit()
        self.search_itemmold.setPlaceholderText("Search item molds…")
        self.search_itemmold.textChanged.connect(
            self.on_search_itemmold
        )
        self.itemmold_table = QTableView()
        self.itemmold_table_model = ItemMoldTableModel()
        self.itemmold_table.setModel(self.itemmold_table_model)
        self.itemmold_table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )
        self.itemmold_table.setSelectionMode(
            QTableView.SelectionMode.SingleSelection
        )
        (
            self.itemmold_table.selectionModel().selectionChanged.connect(
                self.on_itemmold_selected
            )
        )
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_itemmold)
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(self.edit_itemmold)
        self.del_btn = QPushButton("Delete")
        self.del_btn.clicked.connect(self.delete_itemmold)
        left_btn_layout = QHBoxLayout()
        left_btn_layout.addWidget(self.add_btn)
        left_btn_layout.addWidget(self.edit_btn)
        left_btn_layout.addWidget(self.del_btn)
        left = QVBoxLayout()
        left.addWidget(self.search_itemmold)
        left.addWidget(self.itemmold_table)
        left.addLayout(left_btn_layout)
        right = QVBoxLayout()
        self.item_table = QTableView()
        self.item_table_model = ItemTableModel()
        self.item_table.setModel(self.item_table_model)
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
        self.spawn_btn = QPushButton("SPAWN")
        self.spawn_btn.setEnabled(False)
        self.spawn_btn.clicked.connect(self.spawn_item)
        self.destroy_btn = QPushButton("DESTROY")
        self.destroy_btn.setEnabled(False)
        self.destroy_btn.clicked.connect(self.destroy_item)
        right_btn_layout = QHBoxLayout()
        right_btn_layout.addWidget(self.spawn_btn)
        right_btn_layout.addWidget(self.destroy_btn)
        right.addWidget(self.item_table)
        right.addLayout(right_btn_layout)
        layout = QHBoxLayout()
        layout.addLayout(left, 1)
        layout.addLayout(right, 1)
        self.setLayout(layout)
        self.refresh_items()
        self.refresh_molds()

    def refresh_molds(self, search: str | None = None):
        molds = self.itemmold_repo.get_all(search=search)
        self.itemmold_table_model = ItemMoldTableModel(molds)
        self.itemmold_table.setModel(self.itemmold_table_model)
        (
            self.itemmold_table.selectionModel().selectionChanged.connect(
                self.on_itemmold_selected
            )
        )

    def refresh_items(self):
        items = self.item_repo.get_all()
        self.item_model = ItemTableModel(items)
        self.item_table.setModel(self.item_model)

    def spawn_item(self):
        index = self.itemmold_table.selectionModel().selectedRows()[0]
        mold = self.itemmold_table_model.itemmolds[index.row()]
        item = self.item_repo.spawn(mold_id=mold.id, owner=0)
        # self.session.commit()
        self.refresh_items(mold.id)

    def destroy_item(self):
        index = self.item_table.selectionModel().selectedRows()[0]
        item = self.item_model.items[index.row()]
        confirm = QMessageBox.question(
            self,
            "Destroy Item",
            f"Destroy item {item.id}?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        self.item_repo.destroy(item)
        self.refresh_items(item.original_mold)

    @pyqtSlot()
    def on_search_itemmold(self, text: str):
        self.refresh_molds(search=text)

    def delete_itemmold(self):
        indexes = self.itemmold_table.selectionModel().selectedRows()
        if not indexes:
            return
        item = self.itemmold_table_model.itemmolds[indexes[0].row()]
        if not self.confirm_delete(
            "Delete Item Mold",
            "Are you sure you want to delete"
            f"'{item.name}'?\n\n"
            "This action cannot be undone.",
        ):
            return
        self.itemmold_repo.delete(item)
        self.refresh_molds()

    def add_itemmold(self):
        dlg = ItemMoldEditor(self.itemmold_repo, parent=self)
        if dlg.exec():
            self.refresh_molds()

    def edit_itemmold(self):
        indexes = self.itemmold_table.selectionModel().selectedRows()
        if not indexes:
            return
        itemmold = self.itemmold_table_model.itemmolds[
            indexes[0].row()
        ]
        dlg = ItemMoldEditor(
            self.itemmold_repo, itemmold, parent=self
        )
        if dlg.exec():
            self.refresh_molds()

    def confirm_delete(self, title: str, message: str) -> bool:
        reply = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        return reply == QMessageBox.StandardButton.Yes

    @pyqtSlot()
    def on_itemmold_selected(self):
        indexes = self.itemmold_table.selectionModel().selectedRows()
        if not indexes:
            self.spawn_btn.setEnabled(False)
            self.refresh_items(None)
            return
        self.spawn_btn.setEnabled(True)
        mold = self.itemmold_table_model.itemmolds[indexes[0].row()]

    @pyqtSlot()
    def on_item_selected(self):
        has_selection = bool(
            self.item_table.selectionModel().selectedRows()
        )
        self.destroy_btn.setEnabled(has_selection)


class ItemMoldEditor(QDialog):
    def __init__(
        self,
        itemmold_repo,
        itemmold: ItemMold | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.repo = itemmold_repo
        self.itemmold = itemmold
        self.setWindowTitle(
            "Edit Item Mold" if itemmold else "Create Item Mold"
        )
        self.setModal(True)
        self.name_edit = QLineEdit()
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText(
            "Type a tag and press Enter"
        )
        self.tag_list = QListWidget()
        self.tag_list.setFixedHeight(75)
        self.tag_list.setSelectionMode(
            QListWidget.SelectionMode.SingleSelection
        )
        self.tag_list.keyPressEvent = self._tag_list_keypress
        self.completer, self.filter_model = self.build_tag_completer()
        self.tag_input.setCompleter(self.completer)
        self.tag_input.textEdited.connect(self.on_tags_edited)
        self.tag_input.returnPressed.connect(self.commit_tag)
        self.completer.activated.connect(self.commit_tag)
        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(80)
        form = QFormLayout()
        form.addRow("Name", self.name_edit)
        tag_box = QVBoxLayout()
        tag_box.addWidget(self.tag_input)
        tag_box.addWidget(self.tag_list)
        form.addRow("Tags", tag_box)
        form.addRow("Description", self.desc_edit)
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.save_btn.clicked.connect(self.on_save)
        self.cancel_btn.clicked.connect(self.reject)
        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(self.cancel_btn)
        btns.addWidget(self.save_btn)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(btns)
        if self.itemmold:
            self._load_item()

    def _tag_list_keypress(self, event):
        if event.key() in (
            Qt.Key.Key_Delete,
            Qt.Key.Key_Backspace,
        ):
            for item in self.tag_list.selectedItems():
                self.tag_list.takeItem(self.tag_list.row(item))
        else:
            QListWidget.keyPressEvent(self.tag_list, event)

    def _load_item(self):
        self.name_edit.setText(self.itemmold.name)
        self.desc_edit.setText(self.itemmold.description or "")

        for tag in self.itemmold.tags.split(","):
            self.tag_list.addItem(tag.strip())

    @pyqtSlot()
    def on_save(self):
        new_name = self.name_edit.text().strip()
        tags = [
            self.tag_list.item(i).text()
            for i in range(self.tag_list.count())
        ]
        if not tags:
            self._error("At least one tag is required.")
            return
        new_tags = ",".join(tags)
        new_desc = self.desc_edit.toPlainText().strip()
        if not new_name:
            self._error("Name is required.")
            return
            return
        if not new_tags:
            self._error("Tags are required.")
            return
        try:
            if self.itemmold is None:
                self.repo.add(
                    ItemMold(
                        name=new_name,
                        tags=new_tags,
                        description=new_desc or None,
                    )
                )
            else:
                self.repo.update(
                    self.itemmold,
                    name=new_name,
                    tags=new_tags,
                    desc=new_desc or None,
                )
            self.accept()
        except Exception as e:
            self.repo.session.rollback()
            self._error(str(e))

    @pyqtSlot(str)
    def on_tags_edited(self, text):
        self.filter_model.set_filter_text(text)

    @pyqtSlot()
    def commit_tag(self):
        tag = self.tag_input.text().strip()
        if not tag:
            return
        for i in range(self.tag_list.count()):
            if self.tag_list.item(i).text().split(" - ")[0] == tag:
                QTimer.singleShot(0, self.tag_input.clear)
                return
        tag_text = [
            t["text"] for t in ITEMMOLD_TAGS if t["tagname"] == tag
        ][0]
        self.tag_list.addItem(tag + " - " + tag_text)
        QTimer.singleShot(0, self.tag_input.clear)

    def _error(self, message: str):
        QMessageBox.critical(self, "Error", message)

    def build_tag_completer(self):
        display_strings = [f"{t['tagname']}" for t in ITEMMOLD_TAGS]
        base_model = QStringListModel(display_strings)
        filter_model = TagFilterModel()
        filter_model.setSourceModel(base_model)
        completer = QCompleter(filter_model, self)
        completer.setCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCompletionMode(
            QCompleter.CompletionMode.PopupCompletion
        )
        return completer, filter_model
