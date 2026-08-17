from dataclasses import dataclass
from player.domain import Player


@dataclass(frozen=True)
class SleepContext:
    tiredness: int
    sleepyness: int
    anxiety: int
    heat: int


def gather_sleep_context(player: Player) -> SleepContext:
    return SleepContext(
        tiredness=player.stats.get("tiredness"),
        sleepyness=player.stats.get("sleepyness"),
        anxiety=player.stats.get("anxiety"),
        heat=player.stats.get("heat"),
    )


@dataclass(frozen=True)
class WakeUpContext:
    pee: int
    poo: int
    cold: int
    heat: int


def gather_wakeup_context(player: Player) -> WakeUpContext:
    return WakeUpContext(
        pee=player.stats.get("pee"),
        poo=player.stats.get("poo"),
        heat=player.stats.get("heat"),
        cold=player.stats.get("cold"),
    )


@dataclass(frozen=True)
class ThirstContext:
    sweat: int


def gather_thirst_context(player: Player) -> ThirstContext:
    return ThirstContext(sweat=player.stats.get("sweat"))


@dataclass(frozen=True)
class PneumaContext:
    hunger: int
    thirst: int


def gather_pneuma_context(player: Player) -> PneumaContext:
    return PneumaContext(
        hunger=player.stats.get("hunger"),
        thirst=player.stats.get("thirst"),
    )
