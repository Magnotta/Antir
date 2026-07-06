from abc import ABC, abstractmethod
from core.game_state import GameState
from systems.time import Time
from systems.signal_service import Signal


EVENTS = {}


class Event(ABC):
    type: str = "base"
    emits_signals: list[Signal] = []

    def __init__(
        self, due_time: Time, payload: dict | None = None
    ):
        self.payload = payload or {}
        self.due_time = due_time

    def condition(self, state: GameState):
        return True

    @abstractmethod
    def begin(self, state: GameState) -> list:
        pass

    @abstractmethod
    def apply(self, state: GameState):
        pass


class EquipItemEvent(Event):
    type = "equip item"
    emits_signals = [Signal.equipment]

    def begin(self, state) -> list:
        item = state.item_repo.get_item_by_id(
            self.payload["item_id"]
        )
        player = state.get_player_by_id(item.owner_id)
        player.occupy_both_hands()
        return [
            EquipItemEvent(
                state.time + self.payload["equip_delay"],
                payload=self.payload,
            )
        ]

    def apply(self, state):
        item = state.item_repo.get_item_by_id(
            self.payload["item_id"]
        )
        player = state.get_player_by_id(item.owner_id)
        player.equip_item_event(
            item, self.payload["slot_ids"]
        )
        player.free_both_hands()


class ItemOwnershipEvent(Event):
    type = "change item ownership"
    emits_signals = [Signal.inventory]

    def begin(self, state) -> list:
        self.apply(state)
        return []

    def apply(self, state):
        state.item_repo.item_chown(
            self.payload["item_id"],
            self.payload["new_owner_id"],
        )


class PneumaEvent(Event):
    type = "physiological pneuma"
    emits_signals = [Signal.anatomical]

    def __init__(self, due_time, payload=None):
        super().__init__(due_time, payload)

    def begin(self, state):
        self.apply(state)
        return []

    def apply(self, state):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        player.stats.add(
            "pneuma_lost", self.payload["amount"]
        )


class SleepynessEvent(Event):
    type = "player sleepyness"
    emits_signals = [Signal.stats]

    def __init__(self, due_time, payload=None):
        super().__init__(due_time, payload)

    def begin(self, state):
        self.apply(state)
        return []

    def apply(self, state):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        if self.payload["incremental"]:
            player.stats.add(
                "sleepyness", self.payload["amount"]
            )
        else:
            player.stats.set(
                "sleepyness", self.payload["amount"]
            )


class HungerEvent(Event):
    type = "player hunger"
    emits_signals = [Signal.stats]

    def __init__(self, due_time: Time, payload=None):
        super().__init__(due_time, payload)

    def begin(self, state):
        self.apply(state)
        return []

    def apply(self, state):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        player.stats.add("hunger", self.payload["amount"])


class ThirstEvent(Event):
    type = "player thirst"
    emits_signals = [Signal.stats]

    def __init__(self, due_time: Time, payload=None):
        super().__init__(due_time, payload)

    def begin(self, state):
        self.apply(state)
        return []

    def apply(self, state):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        player.stats.add("thirst", self.payload["amount"])


class BoneBreakEvent(Event):
    type = "player bone breaking"
    emits_signals = [Signal.anatomical]

    def __init__(self, due_time, payload=None):
        super().__init__(due_time, payload)

    def begin(self, state):
        self.apply(state)
        return []

    def apply(self, state):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        player.anatomy.set_bodynode_stat(
            self.payload["bodynode"], "broken_bone", True
        )
