from dataclasses import dataclass
from core.game_state import GameState
from player.domain import Player


@dataclass(frozen=True)
class SleepContext:
    tiredness: int
    sleepyness: int
    anxiety: int
    heat: int

    @classmethod
    def gather(cls, player: Player) -> "SleepContext":
        return cls(
            tiredness=player.stats.get("tiredness"),
            sleepyness=player.stats.get("sleepyness"),
            anxiety=player.stats.get("anxiety"),
            heat=player.stats.get("heat"),
        )


@dataclass(frozen=True)
class AsleepContext:
    tiredness: int
    sleepyness: int
    anxiety: int
    heat: int
    sleeping_since: int
    sleep_until: int
    time_now: int

    @classmethod
    def gather(
        cls, state: GameState, player: Player
    ) -> "AsleepContext":
        return cls(
            tiredness=player.stats.get("tiredness"),
            sleepyness=player.stats.get("sleepyness"),
            anxiety=player.stats.get("anxiety"),
            heat=player.stats.get("heat"),
            sleeping_since=player.sleeping_since.tick,
            sleep_until=player.sleep_ref.tick,
            time_now=state.time.tick,
        )


@dataclass(frozen=True)
class ThirstContext:
    sweat: int

    @classmethod
    def gather(cls, player: Player) -> "ThirstContext":
        return cls(sweat=player.stats.get("sweat"))


@dataclass(frozen=True)
class PneumaContext:
    hunger: int
    thirst: int

    @classmethod
    def gather(cls, player: Player) -> "PneumaContext":
        return cls(
            hunger=player.stats.get("hunger"),
            thirst=player.stats.get("thirst"),
        )
