from PyQt6.QtWidgets import (
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
    QLabel,
)

from PyQt6.QtCore import (
    Qt,
    QTimer,
    QModelIndex,
    QStringListModel,
    pyqtSlot,
)
from db.models.item import Mold
from db.repository.item import ItemRepository
from core.defs import (
    MOLD_TAG_DICTS,
    TAG_NAMES,
)
from ..models.param_spec_table import ParamSpecTableModel
from .param_spec_editor import ParamSpecEditor
from ..models.mold_tag_filter import TagFilterModel


class MoldEditor(QDialog):
    def __init__(
        self,
        item_repo: ItemRepository,
        mold: Mold | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle(
            "Edit Item Mold" if mold else "Create Item Mold"
        )
        self.item_repo = item_repo
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
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_spec)
        del_btn = QPushButton("Remove")
        del_btn.clicked.connect(self.remove_spec)
        get_btn = QPushButton("GET")
        get_btn.clicked.connect(self.get_specs_from_tags)
        spec_btns = QHBoxLayout()
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

    def remove_spec(self):
        idx = self.spec_table.currentIndex()
        if idx.isValid():
            self.spec_model.remove_at(idx.row())

    def on_save(self):
        new_name = self.name_edit.text().strip()
        new_tags = ",".join(self.get_tag_list())
        new_desc = self.desc_edit.toPlainText().strip()
        if not new_name:
            QMessageBox.critical(
                self, "Error", "Name is required."
            )
            return
        if not new_tags:
            QMessageBox.critical(
                self,
                "Error",
                "At least one tag is required.",
            )
            return
        try:
            self.mold.name = new_name
            self.mold.tags = new_tags
            self.mold.description = new_desc or None
            errors = self.item_repo.validate_specs(
                self.mold
            )
            if errors:
                QMessageBox.critical(
                    self, "Error", "\n".join(errors)
                )
                return
            if self.is_new:
                self.item_repo.session.add(self.mold)
            self.item_repo.session.commit()
            self.accept()
        except Exception as e:
            self.item_repo.session.rollback()
            QMessageBox.critical(self, "Error", str(e))

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
        created = self.item_repo.create_specs_from_tags(
            self.mold
        )
        if created:
            self.spec_model.layoutChanged.emit()
