from dataclasses import dataclass
from typing import Callable, Sequence
from enum import Enum, auto
from core.events import HungerEvent, EquipItemEvent


class DecisonType(Enum):
    slot_choice = auto()


class PendingDecision:
    def __init__(
        self, decision_type: DecisonType, payload: dict
    ):
        self.type = decision_type
        self.payload = payload


@dataclass(frozen=True)
class CommandSpec:
    key: str
    target_type: str | None
    arg_types: Sequence[type]
    description: str
    handler: Callable


def advance_time(engine, minutes: int):
    for _ in range(minutes):
        engine.step()


def player_hunger(engine):
    engine.schedule(
        HungerEvent(engine.state.time, {"amount": 1}),
        "command",
    )


def move_item(engine, target_list, new_owner_id):
    item = engine.state.item_repo.get_item_by_id(
        target_list[0]
    )
    item.owner_id = new_owner_id


def equip_item(engine, target_list):
    item = engine.state.item_repo.get_item_by_id(
        target_list[0]
    )
    mold = engine.state.item_repo.get_original_mold(item)
    payload = {"item_id": item.id}
    if any(
        [
            True if "right" in slot else False
            for slot in mold.occupied_slots
        ]
    ):
        choice_dict = engine.signals.choice_required(
            PendingDecision(
                DecisonType.slot_choice,
                {"mold_id": mold.id, "item_id": item.id},
            )
        )
        if choice_dict is not None:
            payload["slot_ids"] = choice_dict["slot_ids"]
    else:
        payload["slot_ids"] = mold.occupied_slots
    engine.schedule(
        EquipItemEvent(engine.state.time, payload),
        "command",
    )


COMMANDS = [
    CommandSpec(
        key="tm",
        target_type=None,
        arg_types=[int],
        description="advance time",
        handler=advance_time,
    ),
    CommandSpec(
        key="ph",
        target_type=None,
        arg_types=[],
        description="increase hunger",
        handler=player_hunger,
    ),
    CommandSpec(
        key="ie",
        target_type="Item",
        arg_types=[],
        description="equip item",
        handler=equip_item,
    ),
    CommandSpec(
        key="im",
        target_type="Item",
        arg_types=[int],
        description="item chown",
        handler=move_item,
    ),
]
