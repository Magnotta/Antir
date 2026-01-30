from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTableView, QPushButton,
    QDialog, QLabel, QTextEdit,
    QMessageBox, QFormLayout, QCompleter
)

from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSortFilterProxyModel, QStringListModel
from sqlalchemy import select
from db.models import Item_Mold, itemmold_tags

class TagFilterModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

    def set_filter_text(self, text: str):
        self.setFilterFixedString(text)

    def filterAcceptsRow(self, row, parent):
        if not self.filterRegularExpression().pattern():
            return True

        source = self.sourceModel().index(row, 0, parent)
        return self.filterRegularExpression().pattern().lower() in source.data().lower()

class ItemMoldTableModel(QAbstractTableModel):
    HEADERS = [
        "ID", "Name", "Type", "Tags", "Description"
    ]

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.items: list = []
        self.refresh()

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        item = self.items[index.row()]
        col = index.column()

        return [
            item.id,
            item.name,
            item.type,
            item.tags,
            item.description,
        ][col]

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return section + 1

    def refresh(self, search: str | None = None):
        self.beginResetModel()

        stmt = select(Item_Mold)
        if search:
            stmt = stmt.where(Item_Mold.name.ilike(f"%{search}%"))

        self.items = self.session.scalars(stmt).all()
        self.endResetModel()

    def delete_row(self, row: int):
        item = self.items[row]
        self.session.delete(item)
        self.session.commit()
        self.refresh()



class ItemTab(QWidget):
    def __init__(self, s, parent=None):
        super().__init__(parent)

        self.session = s

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search item molds…")
        self.search.textChanged.connect(self.on_search)

        self.table = QTableView()
        self.model = ItemMoldTableModel(s)
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableView.SelectionMode.SingleSelection
        )

        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_itemmold)

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(self.edit_itemmold)

        self.del_btn = QPushButton("Delete")
        self.del_btn.clicked.connect(self.delete_itemmold)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.del_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self.search)
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)

    def on_search(self, text: str):
        self.model.refresh(search=text)

    def delete_itemmold(self):
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return

        item = self.model.items[indexes[0].row()]

        if not self.confirm_delete(
            "Delete Item Mold",
            f"Are you sure you want to delete '{item.name}'?\n\n" +
            "This action cannot be undone."
        ):
            return

        self.session.delete(item)
        self.session.commit()
        self.model.refresh()

    def add_itemmold(self):
        dlg = ItemMoldEditor(self.session, parent=self)
        if dlg.exec():
            self.model.refresh()

    def edit_itemmold(self):
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return

        item = self.model.items[indexes[0].row()]
        dlg = ItemMoldEditor(self.session, item, parent=self)
        if dlg.exec():
            self.model.refresh()

    def confirm_delete(self, title: str, message: str) -> bool:
        reply = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel
        )

        return reply == QMessageBox.StandardButton.Yes



class ItemMoldEditor(QDialog):
    def __init__(self, session, item: Item_Mold | None = None, parent=None):
        super().__init__(parent)

        self.session = session
        self.item = item

        self.setWindowTitle(
            "Edit Item Mold" if item else "Create Item Mold"
        )
        self.setModal(True)

        self.name_edit = QLineEdit()

        self.type_edit = QLineEdit()
        
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Tags (comma-separated)")
        self.completer, self.filter_model = self.build_tag_completer()
        self.tags_edit.setCompleter(self.completer)
        self.tags_edit.textEdited.connect(self.on_tags_edited)
        self.completer.activated.connect(self.on_tag_selected)
        
        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(80)

        form = QFormLayout()
        form.addRow("Name", self.name_edit)
        form.addRow("Type", self.type_edit)
        form.addRow("Tags", self.tags_edit)
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

        if self.item:
            self._load_item()

    def _load_item(self):
        self.name_edit.setText(self.item.name)
        self.type_edit.setText(self.item.type)
        self.tags_edit.setText(self.item.tags)
        self.desc_edit.setText(self.item.description or "")

    def on_save(self):
        name = self.name_edit.text().strip()
        type_ = self.type_edit.text().strip()
        tags = self.tags_edit.text().strip()
        desc = self.desc_edit.toPlainText().strip()

        if not name:
            self._error("Name is required.")
            return

        if not type_:
            self._error("Type is required.")
            return

        if not tags:
            self._error("Tags are required.")
            return

        try:
            if self.item is None:
                self.item = Item_Mold(
                    name=name,
                    type=type_,
                    tags=tags,
                    description=desc or None
                )
                self.session.add(self.item)
            else:
                self.item.name = name
                self.item.type = type_
                self.item.tags = tags
                self.item.description = desc or None

            self.session.commit()
            self.accept()

        except Exception as e:
            self.session.rollback()
            self._error(str(e))

    def on_tags_edited(self, text: str):
        # Split by commas, autocomplete only last token
        parts = [p.strip() for p in text.split(",")]
        current = parts[-1] if parts else ""

        self.filter_model.set_filter_text(current)

    def on_tag_selected(self, completion: str):
        tagname = completion.split("–")[0].strip()

        parts = [p.strip() for p in self.tags_edit.text().split(",")]

        parts[-1] = tagname
        new_text = ", ".join(parts)

        self.tags_edit.setText(new_text)

    def _error(self, message: str):
        QMessageBox.critical(self, "Error", message)

    def build_tag_completer(self):
        display_strings = [
            f"{t['tagname']}"
            for t in itemmold_tags
        ]

        base_model = QStringListModel(display_strings)
        filter_model = TagFilterModel()
        filter_model.setSourceModel(base_model)

        completer = QCompleter(filter_model, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        return completer, filter_model
