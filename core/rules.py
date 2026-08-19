from enum import IntEnum, auto
from core.events import Event, StatEvent
from systems.signal_service import SignalType, Signal
from .game_state import GameState
from .formulas.sleep_cycle import *
from .formulas.physiology import *
from .formulas.context_gatherers import *


class RuleStrictness(IntEnum):
    ALWAYS = auto()
    PERMISSIVE = auto()
    LENIENT = auto()
    FIRM = auto()
    STRINGENT = auto()
    DRACONIAN = auto()


class Rule:
    listens_to: list[SignalType] = []
    name = "rulebase"
    strictness = RuleStrictness.PERMISSIVE

    def applies(
        self, event: Event, state: GameState
    ) -> bool:
        return True

    def fulfill(
        self, state: GameState, signal: Signal
    ) -> list:
        return []


class SleepyRule(Rule):
    listens_to = [SignalType.hour]
    name = "hourly sleepyness rule"
    category = RuleStrictness.ALWAYS

    def fulfill(self, state, signal):
        return [
            StatEvent(
                state.time,
                {
                    "target": t.player_rec.id,
                    "stat_name": "sleepyness",
                    "amount": baseline_sleepyness(),
                    "incremental": True,
                },
            )
            for t in state.players
            if not t.sleeping_since
        ]


# class WakeUpRule(Rule):
#     listens_to


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
    listens_to = [SignalType.hour]
    name = "hourly thirst rule"
    category = RuleStrictness.FIRM

    def fulfill(self, state, signal):
        return [
            StatEvent(
                state.time,
                {
                    "target": p.player_rec.id,
                    "stat_name": "thirst",
                    "amount": base_thirst(
                        ThirstContext.gather(p)
                    ),
                    "incremental": True,
                },
            )
            for p in state.players
        ]


class PhysioPneumaRule(Rule):
    listens_to = [SignalType.day]
    name = "player physiological pneuma"
    category = RuleStrictness.ALWAYS

    def fulfill(self, state, signal):
        return [
            StatEvent(
                state.time,
                {
                    "target": player.player_rec.id,
                    "stat_name": "pneuma_lost",
                    "amount": base_pneuma(
                        PneumaContext.gather(player)
                    ),
                    "incremental": True,
                },
            )
            for player in state.players
        ]


class DayHungerRule(Rule):
    listens_to = [SignalType.day]
    name = "daily hunger rule"
    category = RuleStrictness.PERMISSIVE

    def fulfill(self, state, signal):
        meal_offsets = [480, 720, 1080]
        return [
            StatEvent(
                state.time + offset,
                {
                    "target": p.player_rec.id,
                    "stat_name": "hunger",
                    "amount": base_hunger(),
                    "incremental": True,
                },
            )
            for p in state.players
            for offset in meal_offsets
        ]


class MidnightHungerRule(Rule):
    listens_to = [SignalType.day]
    name = 'midnight hunger rule'
    category = RuleStrictness.PERMISSIVE

    def fulfill(self, state, signal):
        targets = [
            p.player_rec.id
            for p in state.players
            if p.sleeping_since is None
        ]
        return [
            StatEvent(
                state.time,
                {
                    "target": t,
                    "stat_name": "hunger",
                    "amount": base_hunger(),
                    "incremental": True,
                },
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
