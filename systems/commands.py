from dataclasses import dataclass
from typing import Callable, Sequence
from enum import Enum, auto
import core.events as e


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


def advance_time(engine, minutes: int, message="none"):
    for _ in range(minutes):
        engine.step()


def player_hunger(engine, message="none"):
    engine.schedule(
        e.HungerEvent(
            engine.state.time,
            {"amount": 1, "message": message},
        ),
        "command",
    )


def move_item(engine, target, new_owner_id, message="none"):
    engine.schedule(
        e.ItemOwnershipEvent(
            engine.state.time,
            {
                "item_id": target,
                "new_owner_id": new_owner_id,
                "message": message,
            },
        ),
        "command",
    )


def equip_item(engine, target, message="none"):
    item = engine.state.item_repo.get_item_by_id(target)
    mold = engine.state.item_repo.get_original_mold(item)
    if "eq" not in mold.tags:
        raise ValueError(f"{item.name} is not equippable!")
        return
    if any(
        [
            True if "_" in slot else False
            for slot in mold.occupied_slots
        ]
    ):
        choice_dict = engine.signals.choice_required(
            PendingDecision(
                DecisonType.slot_choice,
                {"mold": mold, "item": item},
            )
        )
        if choice_dict is not None:
            selected_slot_strings = choice_dict["slots_str"]
        else:
            raise ValueError("No slots selected!")
    else:
        selected_slot_strings = mold.occupied_slots
    player = engine.state.get_player_by_id(item.owner_id)
    selected_slots = [
        player.anatomy.get_slot_by_description(
            string.split()[0], string.split()[1]
        )
        for string in selected_slot_strings
    ]
    payload = {
        "item_id": item.id,
        "slot_ids": [slot.id for slot in selected_slots],
        "message": message,
    }
    engine.schedule(
        e.EquipItemEvent(engine.state.time, payload),
        "command",
    )


def export_world(engine, message="none"):
    engine.state.loc_repo.export_world_to_file()


def import_world(engine, message="none"):
    engine.state.loc_repo.import_world_from_file()


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
    CommandSpec(
        key="ew",
        target_type=None,
        arg_types=[],
        description="export world",
        handler=export_world,
    ),
    CommandSpec(
        key="iw",
        target_type=None,
        arg_types=[],
        description="import world",
        handler=import_world,
    ),
]
