from enum import IntEnum, auto
from core.events import (
    Event,
    HungerEvent,
    ThirstEvent,
    PneumaEvent,
    SleepynessEvent,
)
from systems.signal_service import Signal
from .game_state import GameState


class RuleStrictness(IntEnum):
    ALWAYS = auto()
    PERMISSIVE = auto()
    LENIENT = auto()
    FIRM = auto()
    STRINGENT = auto()
    DRACONIAN = auto()


class Rule:
    listens_to: list[Signal] = []
    name = "rulebase"
    strictness = RuleStrictness.PERMISSIVE

    def __init__(self):
        self._state_dict = dict()

    def applies(
        self, event: Event, state: GameState
    ) -> bool:
        return True

    def fulfill(self, state: GameState) -> list:
        return []


class SleepyRule(Rule):
    listens_to = [Signal.hour]
    name = "hourly sleepyness rule"
    category = RuleStrictness.ALWAYS

    def fulfill(self, state):
        return [
            SleepynessEvent(
                state.time,
                {
                    "target": t.player_rec.id,
                    "amount": 150,
                    "incremental": True,
                },
            )
            for t in state.players
        ]


class WakeUpRule(Rule):
    listens_to = [Signal.wake_up]
    name = "wake up rule"
    category = RuleStrictness.ALWAYS

    def fulfill(self, state):
        return [
            SleepynessEvent(
                state.time,
            )
        ]


class EclipticSunRule(Rule):
    pass


class ShitRule(Rule):
    """
    SENSAÇÃO
    Uma cagada forte resolve o problema pelo dia inteiro
    Duas cagadas fracas resolvem também, mas cada uma faz o triplo da sujeira
    Cagada acumulada causa incômodo, eventualmente dor
    Vontade de cagar é uma benção
    """

    pass


class ThirstRule(Rule):
    listens_to = [Signal.hour]
    name = "hourly thirst rule"
    category = RuleStrictness.FIRM

    def fulfill(self, state):
        return [
            ThirstEvent(
                state.time,
                {
                    "target": p.player_rec.id,
                    "amount": 33 + p.stats.get("sweat"),
                },
            )
            for p in state.players
        ]


class PhysioPneumaRule(Rule):
    listens_to = [Signal.day]
    name = "player physiological pneuma"
    category = RuleStrictness.ALWAYS

    def fulfill(self, state):
        pneumas = [-50, -50, -50, -50, -50]
        for player in state.players:
            thirst = player.stats.get("thirst")
            pneumas[player.player_rec.id - 1] += thirst // 5
            hunger = player.stats.get("hunger")
            pneumas[player.player_rec.id - 1] += hunger // 2
        return [
            PneumaEvent(
                state.time,
                {
                    "target": p.player_rec.id,
                    "amount": pneumas[p.player_rec.id - 1],
                },
            )
            for p in state.players
        ]


class DayHungerRule(Rule):
    listens_to = [Signal.day]
    name = 'daily hunger rule'
    category = RuleStrictness.PERMISSIVE

    def fulfill(self, state):
        meal_offsets = [480, 720, 1080]
        return [
            HungerEvent(
                state.time + offset,
                {"target": p.player_rec.id, "amount": 100},
            )
            for offset in meal_offsets
            for p in state.players
        ]


class MidnightHungerRule(Rule):
    listens_to = [Signal.day]
    name = 'midnight hunger rule'
    category = RuleStrictness.PERMISSIVE

    def fulfill(self, state):
        targets = [
            p.player_rec.id
            for p in state.players
            if p.stats.get("sleepyness") > 0
        ]
        return [
            HungerEvent(
                state.time, {"target": t, "amount": 100}
            )
            for t in targets
        ]


RULES: list[Rule] = [
    DayHungerRule(),
    MidnightHungerRule(),
    ThirstRule(),
    PhysioPneumaRule(),
    SleepyRule(),
]
