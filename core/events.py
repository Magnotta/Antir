from abc import ABC, abstractmethod
from core.defs import CHARACTER_STAT_MAX_RATES
from core.game_state import GameState
from core.time import Time
from core.formulas.sleep_cycle import *
from core.formulas.context_gatherers import *
from systems.signal_service import SignalType, Signal


EVENTS = {}


class Event(ABC):
    type: str = "base"

    def __init__(
        self,
        due_time: Time,
        payload: dict | None = None,
        tag: str | None = None,
    ):
        self.payload = payload or {}
        self.due_time = due_time
        self.tag = tag

    def condition(self, state: GameState) -> bool:
        return True

    @abstractmethod
    def begin(
        self, state: GameState
    ) -> tuple[bool, list["Event"]]:
        return (False, [])

    @abstractmethod
    def apply(self, state: GameState) -> list["Event"]:
        return []

    @abstractmethod
    def get_signals(self) -> list[Signal]:
        return []


class PlayerStatCheckEvent(Event, ABC):
    type = "recurring check"

    def begin(self, state):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        remaining = self.payload[
            "threshold"
        ] - player.stats.get(self.payload["stat_name"])
        if remaining < 0:
            return (True, [])
        safe_interval = Time(
            remaining
            // CHARACTER_STAT_MAX_RATES[
                self.payload["stat_name"]
            ]
        )
        next_due = self.due_time + max(safe_interval, 1)
        return (
            False,
            [type(self)(next_due, self.payload, self.tag)],
        )


class WakeUpCheck(PlayerStatCheckEvent):
    type = "player wake up early from stat check"

    def __init__(self, due_time, payload=None, tag=None):
        """
        Payload keys = target
        """
        super().__init__(due_time, payload, tag)

    def apply(self, state):
        return [
            WakeUpEvent(
                state.time,
                self.payload,
                self.tag,
            )
        ]

    def get_signals(self):
        return []


class StatEvent(Event):
    type = "player stat altering event"

    def __init__(self, due_time, payload=None, tag=None):
        """
        Payload keys = target, incremental, stat_name, amount
        """
        super().__init__(due_time, payload, tag)

    def begin(self, state):
        return (True, [])

    def apply(self, state):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        if self.payload["incremental"]:
            player.stats.add(
                self.payload["stat_name"],
                self.payload["amount"],
            )
        else:
            player.stats.set(
                self.payload["stat_name"],
                self.payload["amount"],
            )
        return []

    def get_signals(self):
        return [Signal(SignalType.stats, self.payload)]


class EquipItemEvent(Event):
    type = "equip item"

    def __init__(self, due_time, payload=None, tag=None):
        """
        Payload keys = item_id, slot_ids, equip_delay
        """
        super().__init__(due_time, payload, tag)

    def begin(self, state) -> list:
        item = state.item_repo.get_item_by_id(
            self.payload["item_id"]
        )
        player = state.get_player_by_id(item.owner_id)
        # player.occupy_both_hands()
        return (
            True,
            [
                EquipItemEvent(
                    state.time
                    + self.payload["equip_delay"],
                    payload=self.payload,
                )
            ],
        )

    def apply(self, state):
        item = state.item_repo.get_item_by_id(
            self.payload["item_id"]
        )
        player = state.get_player_by_id(item.owner_id)
        player.equip_item_event(
            item, self.payload["slot_ids"]
        )
        # player.free_both_hands()
        return []

    def get_signals(self):
        return [Signal(SignalType.inventory, self.payload)]


class ItemOwnershipEvent(Event):
    type = "change item ownership"

    def __init__(self, due_time, payload=None, tag=None):
        """
        Payload keys = item_id, new_owner_id
        """
        super().__init__(due_time, payload, tag)

    def begin(self, state) -> list:
        return (True, [])

    def apply(self, state):
        state.item_repo.item_chown(
            self.payload["item_id"],
            self.payload["new_owner_id"],
        )
        return []

    def get_signals(self):
        return [Signal(SignalType.inventory, self.payload)]


class SleepEvent(Event):
    type = "player drift into sleep"

    def __init__(self, due_time, payload=None, tag=None):
        """
        Payload keys = target
        """
        super().__init__(due_time, payload, tag)

    def begin(self, state):
        return (True, [])

    def apply(self, state):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        tag = f"wake_up_player_{player.player_rec.id}"
        pee, poo, heat, cold, duration = wakeup_thresholds(
            SleepContext.gather(player),
            WakeupThreshCoefficients.calculate(player),
        )
        player.sleeping_since = state.time
        player.sleep_ref = state.time + duration
        return [
            WakeUpCheck(
                state.time,
                {
                    "target": player.player_rec.id,
                    "threshold": pee,
                    "stat_name": "pee",
                },
                tag,
            ),
            WakeUpCheck(
                state.time,
                {
                    "target": player.player_rec.id,
                    "threshold": poo,
                    "stat_name": "poo",
                },
                tag,
            ),
            WakeUpCheck(
                state.time,
                {
                    "target": player.player_rec.id,
                    "threshold": heat,
                    "stat_name": "heat",
                },
                tag,
            ),
            WakeUpCheck(
                state.time,
                {
                    "target": player.player_rec.id,
                    "threshold": cold,
                    "stat_name": "cold",
                },
                tag,
            ),
            WakeUpEvent(
                player.sleep_ref,
                {
                    "target": player.player_rec.id,
                },
                tag,
            ),
        ]

    def get_signals(self):
        return [Signal(SignalType.sleep, self.payload)]


class WakeUpEvent(Event):
    type = "player wake up"

    def __init__(self, due_time, payload=None, tag=None):
        """
        Payload keys = target
        """
        super().__init__(due_time, payload, tag)

    def begin(self, state):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        sleepyness, tiredness, anxiety = wakeup_replenish(
            AsleepContext.gather(state, player),
        )
        return (
            True,
            [
                StatEvent(
                    state.time,
                    {
                        "target": self.payload["target"],
                        "stat_name": "sleepyness",
                        "amount": sleepyness,
                        "incremental": False,
                    },
                ),
                StatEvent(
                    state.time,
                    {
                        "target": self.payload["target"],
                        "stat_name": "tiredness",
                        "amount": tiredness,
                        "incremental": False,
                    },
                ),
                StatEvent(
                    state.time,
                    {
                        "target": self.payload["target"],
                        "stat_name": "anxiety",
                        "amount": anxiety,
                        "incremental": False,
                    },
                ),
            ],
        )

    def apply(self, state):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        player.sleeping_since = None
        return []

    def get_signals(self):
        return [Signal(SignalType.wake_up, self.payload)]


class BoneBreakEvent(Event):
    type = "player bone breaking"

    def __init__(self, due_time, payload=None, tag=None):
        """
        Payload keys = target, bodynode
        """
        super().__init__(due_time, payload, tag)

    def begin(self, state):
        return (True, [])

    def apply(self, state):
        player = state.get_player_by_id(
            self.payload["target"]
        )
        player.anatomy.set_bodynode_stat(
            self.payload["bodynode"], "broken_bone", True
        )
        return []

    def get_signals(self):
        return [Signal(SignalType.anatomical, self.payload)]
