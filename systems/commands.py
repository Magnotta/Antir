from dataclasses import dataclass
from typing import Callable, Sequence
import core.events as e
from .pending_decision import DecisonType, PendingDecision
from .engine_interface import EngineProtocol
from .signal_service import Signal


@dataclass(frozen=True)
class CommandSpec:
    key: str
    target_type: str | None
    arg_types: Sequence[type]
    description: str
    handler: Callable


def advance_time(
    engine: EngineProtocol, minutes: int, message="none"
):
    if minutes > 60:
        engine.summarizer.start_batch()
    for _ in range(minutes):
        engine.step()
    if minutes > 60:
        engine.summarizer.end_batch(minutes)
        engine.signals.store([Signal.summary])
        engine.signals.notify()


def player_hunger(engine: EngineProtocol, message="none"):
    engine.schedule(
        e.HungerEvent(
            engine.state.time,
            {"amount": 1, "message": message},
        ),
        "command",
    )


def move_item(
    engine: EngineProtocol,
    target,
    new_owner_id,
    message="none",
):
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


def equip_item(
    engine: EngineProtocol, target, message="none"
):
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
    for param in item.param_list:
        if param.name == "delay":
            delay = param.value
            break
    else:
        raise ValueError(
            f"Item {item.id} doesn't have a delay param!"
        )
    payload = {
        "item_id": item.id,
        "slot_ids": [slot.id for slot in selected_slots],
        "equip_delay": delay,
        "message": message,
    }
    engine.schedule(
        e.EquipItemEvent(engine.state.time, payload),
        "command",
    )


def export_world(engine: EngineProtocol, message="none"):
    engine.state.loc_repo.export_world_to_file()


def import_world(engine: EngineProtocol, message="none"):
    engine.state.loc_repo.import_world_from_file()


def break_bone(
    engine: EngineProtocol, target, message="none"
):
    player = engine.state.get_player_by_id(target)
    choice_dict = engine.signals.choice_required(
        PendingDecision(
            DecisonType.bodynode_choice, {"player": player}
        )
    )
    if choice_dict is not None:
        selected_node_strings = choice_dict["nodes_str"]
    else:
        raise ValueError("No body nodes selected!")
    for string in selected_node_strings:
        engine.schedule(
            e.BoneBreakEvent(
                engine.state.time,
                payload={
                    "bodynode": string,
                    "target": target,
                },
            ),
            "command",
        )


def go_to_sleep(
    engine: EngineProtocol, target, message="none"
):
    player = engine.state.get_player_by_id(target)
    delta = 0
    engine.schedule(
        e.SleepynessEvent(
            engine.state.time + delta,
            {
                "target": target,
                "amount": 0,
                "incremental": False,
            },
        ),
        "command",
    )
    # player.stats.set("sleepyness", 0)


COMMANDS = {
    "tm": CommandSpec(
        key="tm",
        target_type=None,
        arg_types=[int],
        description="advance time",
        handler=advance_time,
    ),
    "ph": CommandSpec(
        key="ph",
        target_type=None,
        arg_types=[],
        description="increase hunger",
        handler=player_hunger,
    ),
    "ie": CommandSpec(
        key="ie",
        target_type="item",
        arg_types=[],
        description="equip item",
        handler=equip_item,
    ),
    "im": CommandSpec(
        key="im",
        target_type="item",
        arg_types=[int],
        description="item chown",
        handler=move_item,
    ),
    "ew": CommandSpec(
        key="ew",
        target_type=None,
        arg_types=[],
        description="export world",
        handler=export_world,
    ),
    "iw": CommandSpec(
        key="iw",
        target_type=None,
        arg_types=[],
        description="import world",
        handler=import_world,
    ),
    "pbb": CommandSpec(
        key="pbb",
        target_type="player",
        arg_types=[],
        description="break a bone",
        handler=break_bone,
    ),
    "pgs": CommandSpec(
        key="pgs",
        target_type="player",
        arg_types=[],
        description="go to sleep",
        handler=go_to_sleep,
    ),
}
