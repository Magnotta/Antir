from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QDialog,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)
from core.engine import Engine
from systems.signal_service import Signal
from systems.commands import DecisonType
from ui.home_tab import HomeTab
from ui.item_tab import ItemTab
from ui.player_tab import PlayersTab


class SlotChoiceDialog(QDialog):
    def __init__(self, mold, repo, parent=None):
        super().__init__(parent)
        self.mold = mold
        self.repo = repo
        self.setModal(True)
        self.setWindowTitle(f"Occupied Slots – {mold.name}")
        self.all_slots = QListWidget()
        self.used_slots = QListWidget()
        for slot in mold.occupied_slots:
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
        accept = QPushButton("Accept")
        cancel = QPushButton("Cancel")
        accept.clicked.connect(self.on_accept)
        cancel.clicked.connect(self.reject)
        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(cancel)
        btns.addWidget(accept)
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

    def selected_slots(self):
        slot_strings = [
            self.used_slots.item(i).text()
            for i in range(self.used_slots.count())
        ]
        return slot_strings

    def on_accept(self):
        slot_strings = [
            self.used_slots.item(i).text()
            for i in range(self.used_slots.count())
        ]
        body_parts = [
            string.split()[0] for string in slot_strings
        ]
        for part in body_parts:
            if "_" in part:
                body_side, body_part = part.split("_")
                for part_aux in body_parts:
                    if body_side == "left":
                        if (
                            part_aux.split("_")[0]
                            == "right"
                            and part_aux.split("_")[1]
                            == body_part
                        ):
                            QMessageBox.critical(
                                self,
                                "Error",
                                "Cannot have left and right of the same body part!",
                            )
                            return
                    else:
                        if (
                            part_aux.split("_")[0] == "left"
                            and part_aux.split("_")[1]
                            == body_part
                        ):
                            QMessageBox.critical(
                                self,
                                "Error",
                                "Cannot have left and right of the same body part!",
                            )
                            return
        self.mold.occupied_slots = slot_strings
        self.accept()


class Window(QMainWindow):
    def __init__(
        self,
        engine: Engine,
        item_repo,
    ):
        super().__init__()
        self.setWindowTitle("Antir, otários")
        self.resize(800, 600)
        self.engine = engine
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.home_tab = HomeTab(self.engine)
        self.item_tab = ItemTab(
            item_repo,
            self,
        )
        self.player_tab = PlayersTab(engine.state.players)
        self.engine.signals.connect(
            Signal.inventory, self.player_tab.refresh
        )
        self.engine.signals.connect(
            Signal.equipment, self.player_tab.refresh
        )
        self.engine.signals.connect(
            Signal.stats, self.player_tab.refresh
        )
        self.engine.signals.connect(
            Signal.minute, self.home_tab.refresh
        )
        self.engine.signals.connect(
            Signal.location, self.home_tab.refresh
        )
        self.engine.signals.create_decision_path(
            DecisonType.slot_choice,
            self.slot_choice_required,
        )
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.item_tab, "Items")
        self.tabs.addTab(self.player_tab, "Players")

    def slot_choice_required(self, payload):
        mold = self.engine.state.item_repo.get_mold_by_id(
            payload["mold_id"]
        )
        dlg = SlotChoiceDialog(
            mold, self.engine.state.item_repo, parent=self
        )
        if dlg.exec():
            selected_slot_strings = dlg.selected_slots()
            item = (
                self.engine.state.item_repo.get_item_by_id(
                    payload["item_id"]
                )
            )
            player = self.engine.state.get_player_by_id(
                item.owner_id
            )
            selected_slots = [
                player.anatomy.get_slot_by_description(
                    string.split()[0], string.split()[1]
                )
                for string in selected_slot_strings
            ]
            return {
                "item_id": payload["item_id"],
                "slot_ids": [
                    slot.id for slot in selected_slots
                ],
            }
