from enum import IntEnum, auto
from core.events import HungerEvent, ThirstEvent
from systems.signal_service import Signal


class RuleStrictness(IntEnum):
    PERMISSIVE = auto()
    LENIENT = auto()
    FIRM = auto()
    STRINGENT = auto()
    DRACONIAN = auto()


class Rule:
    listens_to: list[Signal] = []
    name = 'rulebase'
    strictness = RuleStrictness.PERMISSIVE

    def __init__(self):
        self._state_dict = dict()

    def applies(self, event, state) -> bool:
        return True

    def fulfill(self, state) -> list:
        return []


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
    """
    SENSAÇÃO
    Suar causa sede
    Dormir causa sede
    Comer causa sede
    Sede causa preguiça
    Dormir com sede causa desidratação
    Beber pouca água elimina a sede momentânea mas não previne desidratação
    """

    listens_to = [Signal.hour]
    name = 'hourly thirst rule'
    category = RuleStrictness.FIRM

    def fulfill(self, state):
        return [
            ThirstEvent(
                state.time, {"target": 1, "amount": 10}
            ),
            ThirstEvent(
                state.time, {"target": 2, "amount": 10}
            ),
            ThirstEvent(
                state.time, {"target": 3, "amount": 10}
            ),
            ThirstEvent(
                state.time, {"target": 4, "amount": 10}
            ),
            ThirstEvent(
                state.time, {"target": 5, "amount": 10}
            ),
        ]


class DehydrationRule(Rule):
    pass


class DayHungerRule(Rule):
    listens_to = [Signal.day]
    name = 'daily hunger rule'
    category = RuleStrictness.PERMISSIVE

    def fulfill(self, state):
        return [
            HungerEvent(
                state.time + 480,
                {"target": 1, "amount": 1},
            ),
            HungerEvent(
                state.time + 480,
                {"target": 2, "amount": 1},
            ),
            HungerEvent(
                state.time + 480,
                {"target": 3, "amount": 1},
            ),
            HungerEvent(
                state.time + 480,
                {"target": 4, "amount": 1},
            ),
            HungerEvent(
                state.time + 480,
                {"target": 5, "amount": 1},
            ),
            HungerEvent(
                state.time + 720,
                {"target": 1, "amount": 1},
            ),
            HungerEvent(
                state.time + 720,
                {"target": 2, "amount": 1},
            ),
            HungerEvent(
                state.time + 720,
                {"target": 3, "amount": 1},
            ),
            HungerEvent(
                state.time + 720,
                {"target": 4, "amount": 1},
            ),
            HungerEvent(
                state.time + 720,
                {"target": 5, "amount": 1},
            ),
            HungerEvent(
                state.time + 1080,
                {"target": 1, "amount": 1},
            ),
            HungerEvent(
                state.time + 1080,
                {"target": 2, "amount": 1},
            ),
            HungerEvent(
                state.time + 1080,
                {"target": 3, "amount": 1},
            ),
            HungerEvent(
                state.time + 1080,
                {"target": 4, "amount": 1},
            ),
            HungerEvent(
                state.time + 1080,
                {"target": 5, "amount": 1},
            ),
        ]


class MidnightHungerRule(Rule):
    listens_to = [Signal.day]
    name = 'midnight hunger rule'
    category = RuleStrictness.PERMISSIVE

    def fulfill(self, state):
        targets = [
            p.player_rec.id
            for p in state.players
            if p.stats.get("awake") > 0
        ]
        return [
            HungerEvent(
                state.time, {"target": t, "amount": 1}
            )
            for t in targets
        ]


RULES = [
    DayHungerRule(),
    MidnightHungerRule(),
    ThirstRule(),
]
