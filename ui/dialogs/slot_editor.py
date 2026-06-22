from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QDialog,
    QListWidget,
)
from core.defs import (
    SLOTS_LIST,
)


class OccupiedSlotsEditorDialog(QDialog):
    def __init__(self, mold, repo, parent=None):
        super().__init__(parent)
        self.mold = mold
        self.repo = repo
        self.setModal(True)
        self.setWindowTitle(f"Occupied Slots – {mold.name}")
        self.all_slots = QListWidget()
        self.used_slots = QListWidget()
        for slot in SLOTS_LIST:
            self.all_slots.addItem(slot)
        for slot in mold.occupied_slots or []:
            self.used_slots.addItem(slot)
        add_btn = QPushButton("→")
        remove_btn = QPushButton("←")
        add_btn.clicked.connect(self.add_slot)
        remove_btn.clicked.connect(self.remove_slot)
        arrows = QVBoxLayout()
        arrows.addStretch()
        arrows.addWidget(add_btn)
        arrows.addWidget(remove_btn)
        arrows.addStretch()
        lists = QHBoxLayout()
        lists.addWidget(self.all_slots)
        lists.addLayout(arrows)
        lists.addWidget(self.used_slots)
        save = QPushButton("Save")
        cancel = QPushButton("Cancel")
        save.clicked.connect(self.on_save)
        cancel.clicked.connect(self.reject)
        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(cancel)
        btns.addWidget(save)
        layout = QVBoxLayout(self)
        layout.addLayout(lists)
        layout.addLayout(btns)

    def add_slot(self):
        item = self.all_slots.currentItem()
        if not item:
            return

        text = item.text()
        if not self._exists(self.used_slots, text):
            self.used_slots.addItem(text)

    def remove_slot(self):
        row = self.used_slots.currentRow()
        if row >= 0:
            self.used_slots.takeItem(row)

    def _exists(self, list_widget, text):
        for i in range(list_widget.count()):
            if list_widget.item(i).text() == text:
                return True
        return False

    def on_save(self):
        self.mold.occupied_slots = [
            self.used_slots.item(i).text()
            for i in range(self.used_slots.count())
        ]
        self.accept()
