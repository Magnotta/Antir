from dataclasses import dataclass
from typing import Callable, Sequence
from core.events import HungerEvent


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


COMMANDS = [
    CommandSpec(
        key="tm",
        target_type=None,
        arg_types=[int],
        description="Advance time (minutes)",
        handler=advance_time,
    ),
    CommandSpec(
        key="ph",
        target_type=None,
        arg_types=[],
        description="Increase hunger",
        handler=player_hunger,
    ),
]
