from core.events import (
    HungerEvent,
)
from systems.time_service import Time


class Rule:
    listens_to: list[str] = []
    name = 'rulebase'

    def __init__(self):
        self._state_dict = dict()

    def applies(self, event, state) -> bool:
        return True

    def fulfill(self, state) -> list:
        return []


class DayHungerRule(Rule):
    listens_to = ['day']
    name = 'daily hunger rule'

    def fulfill(self, state):
        return [
            HungerEvent(
                state.time + Time(480),
                {"target": 1, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(480),
                {"target": 2, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(480),
                {"target": 3, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(480),
                {"target": 4, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(480),
                {"target": 5, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(720),
                {"target": 1, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(720),
                {"target": 2, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(720),
                {"target": 3, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(720),
                {"target": 4, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(720),
                {"target": 5, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(1080),
                {"target": 1, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(1080),
                {"target": 2, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(1080),
                {"target": 3, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(1080),
                {"target": 4, "amount": 1},
            ),
            HungerEvent(
                state.time + Time(1080),
                {"target": 5, "amount": 1},
            ),
        ]


class MidnightHungerRule(Rule):
    listens_to = ['day']
    name = 'midnight hunger rule'

    def fulfill(self, state):
        targets = [
            p.player_rec.id
            for p in state.players
            if p.stats.get("awake") > 0
        ]
        return [
            HungerEvent(state.time, {"target": t, "amount": 1})
            for t in targets
        ]


RULES = [
    DayHungerRule(),
    MidnightHungerRule(),
]
