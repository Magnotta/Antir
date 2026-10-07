from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget,
)
from core.engine import Engine
from systems.signal_service.signal_service import SignalType
from systems.command_service.commands import DecisonType
from .tabs.home import HomeTab
from .tabs.item import ItemTab
from .tabs.player import PlayersTab
from .tabs.loc import LocalityTab
from .dialogs.choice_answer import ChoiceDialog
from .dialogs.task_spec_dialog import TaskSpecDialog
from .widgets.summarizer_popup import SummarizerPopup


class Window(QMainWindow):
    def __init__(self, engine: Engine):
        super().__init__()
        self.setWindowTitle("Antir, otários")
        self.resize(800, 600)
        self.engine = engine
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.home_tab = HomeTab(self.engine)
        self.item_tab = ItemTab(
            self.engine.state.item_repo,
            self,
        )
        self.player_tab = PlayersTab(engine.state.players)
        self.loc_tab = LocalityTab(
            self.engine.state.loc_repo, self.engine.state
        )
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.item_tab, "Items")
        self.tabs.addTab(self.player_tab, "Players")
        self.tabs.addTab(self.loc_tab, "Locations")
        self.engine.signals.connect(
            SignalType.inventory, self.player_tab.refresh
        )
        self.engine.signals.connect(
            SignalType.equipment, self.player_tab.refresh
        )
        self.engine.signals.connect(
            SignalType.stats, self.player_tab.refresh
        )
        self.engine.signals.connect(
            SignalType.minute,
            self.home_tab.refresh_location,
        )
        self.engine.signals.connect(
            SignalType.location,
            self.home_tab.refresh_location,
        )
        self.engine.signals.connect(
            SignalType.summary, self.on_summary_ready
        )
        self.engine.signals.connect(
            SignalType.weather, self.update_home_background
        )
        self.engine.signals.connect(
            SignalType.new_task, self.create_task
        )
        self.engine.signals.create_decision_path(
            DecisonType.slot_choice,
            self.slot_choice_required,
        )
        self.engine.signals.create_decision_path(
            DecisonType.bodynode_choice,
            self.bodynode_choice_required,
        )

    def slot_choice_required(self, payload):
        mold = payload["mold"]

        dlg = ChoiceDialog(
            mold.occupied_slots,
            validation_func=validate_body_parts,
            parent=self,
        )

        if dlg.exec():
            selected_slot_strings = dlg.selected_options()
            item = payload["item"]
            return {
                "item": item,
                "slots_str": selected_slot_strings,
            }

    def bodynode_choice_required(self, payload):
        player = self.engine.state.get_player_by_id(
            payload["player"]
        )

        dlg = ChoiceDialog(
            player.anatomy.by_name.keys(), parent=self
        )

        if dlg.exec():
            selected_bodynode_strings = (
                dlg.selected_options()
            )
            return {
                "player": player,
                "nodes_str": selected_bodynode_strings,
            }

    def on_summary_ready(self):
        """Slot called when the summarizer finishes a batch."""
        summary_text = (
            self.engine.summarizer.get_last_summary()
        )
        current_tick = self.engine.state.time.tick
        popup = SummarizerPopup(
            summary_text, current_tick, parent=self
        )
        popup.exec()

    def update_home_background(self):
        self.home_tab.update()

    def create_task(self):
        spec = TaskSpecDialog.get_task_spec(
            item_repository=self.engine.state.item_repo,
            participant_ids=[],
            parent=self,
        )
        if spec is not None:
            return


def validate_body_parts(selected: list) -> tuple[bool, str]:
    body_parts = [s.split()[0] for s in selected]
    for part in body_parts:
        if "_" in part:
            side, bp = part.split("_")
            opposite = "right" if side == "left" else "left"
            opposite_part = f"{opposite}_{bp}"
            if opposite_part in body_parts:
                return (
                    False,
                    f"Cannot have both {part} and {opposite_part}!",
                )
    return True, ""
