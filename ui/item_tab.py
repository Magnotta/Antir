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
    QAbstractItemView,
    QDoubleSpinBox,
    QLabel,
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
from db.models import Mold, Item, ItemParam, ParamSpec
from db.repository import (
    SpecRepository,
    MoldRepository,
    ParamRepository,
    ItemRepository,
)
from core.defs import MOLD_TAG_DICTS, TAG_NAMES


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


class ParamSpecTableModel(QAbstractTableModel):
    HEADERS = ["Param", "Base", "Variance"]

    def __init__(self, specs: list[ParamSpec], parent=None):
        super().__init__(parent)
        self.specs = specs

    def rowCount(self, parent=QModelIndex()):
        return len(self.specs)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return section + 1

    def data(self, index, role):
        if not index.isValid():
            return None

        spec = self.specs[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            return [
                spec.param,
                spec.base,
                spec.variance,
            ][col]

        return None

    def add_spec(self, spec: ParamSpec):
        self.beginInsertRows(
            QModelIndex(), len(self.specs), len(self.specs)
        )
        self.specs.append(spec)
        self.endInsertRows()

    def remove_at(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.specs[row]
        self.endRemoveRows()


class ItemParamTableModel(QAbstractTableModel):
    HEADERS = ["Param", "Value"]

    def __init__(
        self, params: list[ItemParam], parent=None
    ):
        super().__init__(parent)
        self.params = params

    def rowCount(self, parent=QModelIndex()):
        return len(self.params)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return section + 1

    def data(self, index, role):
        if not index.isValid():
            return None

        param = self.params[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            return [
                param.name,
                param.value,
            ][col]


class MoldTableModel(QAbstractTableModel):
    HEADERS = ["ID", "Name", "Tags", "Description"]

    def __init__(self, molds: list[Mold] = []):
        super().__init__()
        self.molds = molds

    def rowCount(self, parent=QModelIndex()):
        return len(self.molds)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if (
            not index.isValid()
            or role != Qt.ItemDataRole.DisplayRole
        ):
            return None
        item = self.molds[index.row()]
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
        item = self.molds[row]
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
        if (
            not index.isValid()
            or role != Qt.ItemDataRole.DisplayRole
        ):
            return None
        item = self.items[index.row()]
        col = index.column()
        return [
            item.id,
            item.original_mold_id,
            item.owner_id,
            item.container_item_id,
        ][col]

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
        spec_repo: SpecRepository,
        mold_repo: MoldRepository,
        param_repo: ParamRepository,
        item_repo: ItemRepository,
        parent=None,
    ):
        super().__init__(parent)
        self.spec_repo = spec_repo
        self.mold_repo = mold_repo
        self.param_repo = param_repo
        self.item_repo = item_repo
        self.search_mold = QLineEdit()
        self.search_mold.setPlaceholderText("Search molds…")
        self.search_mold.textChanged.connect(
            self.on_search_mold
        )
        self.mold_table = QTableView()
        self.mold_table_model = MoldTableModel()
        self.mold_table.setModel(self.mold_table_model)
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
        left_btn_layout = QHBoxLayout()
        left_btn_layout.addWidget(self.add_mold_btn)
        left_btn_layout.addWidget(self.edit_mold_btn)
        left_btn_layout.addWidget(self.del_mold_btn)
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

    def refresh_molds(self, search: str | None = None):
        molds = self.mold_repo.get_all(search=search)
        self.mold_table_model = MoldTableModel(molds)
        self.mold_table.setModel(self.mold_table_model)
        (
            self.mold_table.selectionModel().selectionChanged.connect(
                self.on_mold_selected
            )
        )

    def refresh_items(self, search: str | None = None):
        items = self.item_repo.get_all(search=search)
        self.item_table_model = ItemTableModel(items)
        self.item_table.setModel(self.item_table_model)
        (
            self.item_table.selectionModel().selectionChanged.connect(
                self.on_item_selected
            )
        )

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
                self.param_repo,
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
        item = self.item_model.items[index.row()]
        confirm = QMessageBox.question(
            self,
            "Destroy Item",
            f"Destroy item with ID {item.id}?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        self.item_repo.destroy(item)
        self.refresh_items(item.original_mold_id)

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
        self.mold_repo.delete(item)
        self.refresh_molds()

    def add_mold(self):
        dlg = MoldEditor(
            self.spec_repo, self.mold_repo, parent=self
        )
        if dlg.exec():
            self.refresh_molds()

    def on_mold_double_clicked(self, index: QModelIndex):
        if not index.isValid():
            return
        row = index.row()
        mold = self.mold_table_model.molds[row]
        dlg = MoldEditor(
            self.spec_repo, self.mold_repo, mold=mold
        )
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
            self.spec_repo,
            self.mold_repo,
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


class ParamSpecEditor(QDialog):
    def __init__(
        self, spec: ParamSpec | None = None, parent=None
    ):
        super().__init__(parent)
        self.setWindowTitle("Edit Parameter Spec")
        self.param_edit = QLineEdit()
        self.base_edit = QDoubleSpinBox()
        self.var_edit = QDoubleSpinBox()
        for box in (
            self.base_edit,
            self.var_edit,
        ):
            box.setRange(0, 1000)
        form = QFormLayout()
        form.addRow("Param", self.param_edit)
        form.addRow("Base", self.base_edit)
        form.addRow("Variance", self.var_edit)
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(btn_cancel)
        btns.addWidget(btn_ok)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(btns)
        if spec:
            self.param_edit.setText(spec.param)
            self.base_edit.setValue(spec.base)
            self.var_edit.setValue(spec.variance)

    def get_data(self):
        return dict(
            param=self.param_edit.text().strip(),
            base=self.base_edit.value(),
            variance=self.var_edit.value(),
        )


class MoldEditor(QDialog):
    def __init__(
        self,
        spec_repo: SpecRepository,
        mold_repo: MoldRepository,
        mold: Mold | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle(
            "Edit Item Mold" if mold else "Create Item Mold"
        )
        self.spec_repo = spec_repo
        self.mold_repo = mold_repo
        if mold is None:
            self.mold = Mold(
                name="",
                tags="",
                description=None,
                param_specs=[],
            )
            self.is_new = True
        else:
            self.mold = mold
            self.is_new = False
        self.setModal(True)
        self.completer, self.filter_model = (
            self.build_tag_completer()
        )
        self.completer.activated.connect(self.commit_tag)
        self.name_edit = QLineEdit()
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText(
            "Type a tag and press Enter"
        )
        self.tag_input.setCompleter(self.completer)
        self.tag_input.textEdited.connect(
            self.on_tags_edited
        )
        self.tag_input.returnPressed.connect(
            self.commit_tag
        )
        self.tag_list = QListWidget()
        self.tag_list.setFixedHeight(75)
        self.tag_list.setSelectionMode(
            QListWidget.SelectionMode.SingleSelection
        )
        self.tag_list.keyPressEvent = (
            self._tag_list_keypress
        )
        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(80)
        self.spec_model = ParamSpecTableModel(
            self.mold.param_specs
        )
        self.spec_table = QTableView()
        self.spec_table.setModel(self.spec_model)
        self.spec_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.spec_table.doubleClicked.connect(
            self.on_spec_double_clicked
        )
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_spec)
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_spec)
        del_btn = QPushButton("Remove")
        del_btn.clicked.connect(self.remove_spec)
        get_btn = QPushButton("GET")
        get_btn.clicked.connect(self.get_specs_from_tags)
        spec_btns = QHBoxLayout()
        spec_btns.addWidget(add_btn)
        spec_btns.addWidget(edit_btn)
        spec_btns.addWidget(del_btn)
        spec_btns.addWidget(get_btn)
        tag_box = QVBoxLayout()
        tag_box.addWidget(self.tag_input)
        tag_box.addWidget(self.tag_list)
        form = QFormLayout()
        form.addRow("Name", self.name_edit)
        form.addRow("Tags", tag_box)
        form.addRow("Description", self.desc_edit)
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.save_btn.clicked.connect(self.on_save)
        self.cancel_btn.clicked.connect(self.reject)
        bottom = QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(self.cancel_btn)
        bottom.addWidget(self.save_btn)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(QLabel("Parameter Specs"))
        layout.addWidget(self.spec_table)
        layout.addLayout(spec_btns)
        layout.addLayout(bottom)
        if not self.is_new:
            self._load_item()

    def on_spec_double_clicked(self, index: QModelIndex):
        if not index.isValid():
            return
        row = index.row()
        spec = self.spec_model.specs[row]
        dlg = ParamSpecEditor(spec, self)
        if dlg.exec():
            data = dlg.get_data()
            for key, value in data.items():
                setattr(spec, key, value)
            self.spec_model.dataChanged.emit(
                self.spec_model.index(row, 0),
                self.spec_model.index(
                    row, self.spec_model.columnCount() - 1
                ),
            )

    def edit_spec(self):
        idx = self.spec_table.currentIndex()
        if not idx.isValid():
            return
        spec = self.spec_model.specs[idx.row()]
        dlg = ParamSpecEditor(spec, self)
        if dlg.exec():
            data = dlg.get_data()
            for k, v in data.items():
                setattr(spec, k, v)
            self.spec_model.layoutChanged.emit()

    def _tag_list_keypress(self, event):
        if event.key() in (
            Qt.Key.Key_Delete,
            Qt.Key.Key_Backspace,
        ):
            for item in self.tag_list.selectedItems():
                self.tag_list.takeItem(
                    self.tag_list.row(item)
                )
        else:
            QListWidget.keyPressEvent(self.tag_list, event)

    def _load_item(self):
        self.name_edit.setText(self.mold.name)
        self.desc_edit.setText(self.mold.description or "")
        for tag in self.mold.tags.split(","):
            self.tag_list.addItem(tag.strip())

    def get_tag_list(self):
        return [
            self.tag_list.item(i).text().split(" - ")[0]
            for i in range(self.tag_list.count())
        ]

    def add_spec(self):
        dlg = ParamSpecEditor(parent=self)
        if dlg.exec():
            data = dlg.get_data()
            spec = ParamSpec(**data)
            self.spec_model.add_spec(spec)

    def remove_spec(self):
        idx = self.spec_table.currentIndex()
        if idx.isValid():
            self.spec_model.remove_at(idx.row())

    def on_save(self):
        new_name = self.name_edit.text().strip()
        new_tags = ",".join(self.get_tag_list())
        new_desc = self.desc_edit.toPlainText().strip()
        if not new_name:
            self._error("Name is required.")
            return
        if not new_tags:
            self._error("At least one tag is required.")
            return
        try:
            self.mold.name = new_name
            self.mold.tags = new_tags
            self.mold.description = new_desc or None
            errors = self.spec_repo.validate_specs(
                self.mold
            )
            if errors:
                self._error("\n".join(errors))
                return
            if self.is_new:
                self.mold_repo.session.add(self.mold)
            self.mold_repo.session.commit()
            self.accept()
        except Exception as e:
            self.mold_repo.session.rollback()
            self._error(str(e))

    def on_tags_edited(self, text):
        self.filter_model.set_filter_text(text)

    def commit_tag(self):
        tag = self.tag_input.text().strip()
        if not tag:
            return
        if tag not in TAG_NAMES:
            return
        if tag in self.get_tag_list():
            QTimer.singleShot(0, self.tag_input.clear)
            return
        tag_text = [
            t["text"]
            for t in MOLD_TAG_DICTS
            if t["tag_name"] == tag
        ][0]
        self.tag_list.addItem(tag + " - " + tag_text)
        QTimer.singleShot(0, self.tag_input.clear)

    def _error(self, message: str):
        QMessageBox.critical(self, "Error", message)

    def build_tag_completer(self):
        display_strings = [
            t["tag_name"] for t in MOLD_TAG_DICTS
        ]
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

    @pyqtSlot()
    def get_specs_from_tags(self):
        tags = self.get_tag_list()
        if not tags:
            QMessageBox.warning(
                self, "No tags", "Add tags first."
            )
            return
        self.mold.tags = ",".join(tags)
        created = self.spec_repo.create_specs_from_tags(
            self.mold
        )
        if created:
            self.spec_model.layoutChanged.emit()


class SpawnItemDialog(QDialog):
    def __init__(
        self,
        item_repo: ItemRepository,
        mold: Mold,
        parent=None,
    ):
        super().__init__(parent)
        self.mold = mold
        self.manual_fields: dict[str, QDoubleSpinBox] = {}
        self.setWindowTitle(f"Spawn Item – {mold.name}")
        self.setModal(True)
        layout = QVBoxLayout(self)
        info = QLabel(
            "Fill in the required parameters for this item."
        )
        info.setWordWrap(True)
        layout.addWidget(info)
        form = QFormLayout()
        for (
            param_dict
        ) in item_repo.get_manual_param_defaults(mold):
            spin = QDoubleSpinBox()
            spin.setDecimals(0)
            spin.setRange(0, param_dict["max"])
            spin.setValue(param_dict["value"])
            self.manual_fields[param_dict["param"]] = spin
            form.addRow(param_dict["param"], spin)
        if not self.manual_fields:
            form.addRow(
                QLabel("No manual parameters required.")
            )
        layout.addLayout(form)
        btn_spawn = QPushButton("Spawn")
        btn_cancel = QPushButton("Cancel")
        btn_spawn.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(btn_cancel)
        btns.addWidget(btn_spawn)
        layout.addLayout(btns)

    def get_manual_params(self) -> dict[str, int]:
        return {
            param: widget.value()
            for param, widget in self.manual_fields.items()
        }


class ItemEditorDialog(QDialog):
    def __init__(
        self, item: Item, repo: ItemRepository, parent=None
    ):
        super().__init__(parent)
        self.item = item
        self.repo = repo
        self.inputs = {}
        self.setWindowTitle(f"Edit Item #{item.id}")
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        for param in self.item.param_list:
            spin = QDoubleSpinBox()
            spin.setMinimum(0)
            spin.setMaximum(self.repo.get_param_max(param))
            spin.setValue(param.value)
            spin.setDecimals(0)
            self.inputs[param.name] = spin
            form.addRow(param.name, spin)
        layout.addLayout(form)
        btns = QHBoxLayout()
        btns.addStretch()
        cancel = QPushButton("Cancel")
        save = QPushButton("Save")
        cancel.clicked.connect(self.reject)
        save.clicked.connect(self.on_save)
        btns.addWidget(cancel)
        btns.addWidget(save)
        layout.addLayout(btns)

    def on_save(self):
        try:
            for param, widget in self.inputs.items():
                value = widget.value()
                self._set_param(param, value)

            self.repo.session.commit()
            self.accept()

        except Exception as e:
            self.repo.session.rollback()
            QMessageBox.critical(self, "Error", str(e))

    def _set_param(self, param, value):
        for p in self.item.param_list:
            if p.name == param:
                p.value = value
                return
