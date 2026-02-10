from db.repository import (
    EventRepository,
    ItemRepository,
    PlayerRepository,
)
from core.game_state import GameState
from core.rules import RULES
from player.domain import Player
from systems.command_service import CommandService
from systems.signal_service import SignalBus


class Engine:
    def __init__(
        self,
        event_repo: EventRepository,
        item_repo: ItemRepository,
        player_repo: PlayerRepository,
        players: list[Player],
    ):
        self.state = GameState(players)
        self.event_repo = event_repo
        self.item_repo = item_repo
        self.player_repo = player_repo
        self.cmd = CommandService(self)
        self.events = []
        self.rules = RULES
        self.signals = SignalBus()

    def schedule(self, event, org: str):
        self.event_repo.add_record(event, org)
        self.events.append(event)
        self.events.sort(key=lambda e: e.due_time)

    def step(self):
        self._advance_time()
        self._dispatch_due_events()

    def _advance_time(self):
        self.state.time += 1
        self.signals.store('minute')
        if self.state.time.hour_change:
            self.signals.store('hour')
        if self.state.time.day_change:
            self.signals.store('day')

    def _dispatch_due_events(self):
        due = [
            e
            for e in self.events
            if e.due_time <= self.state.time
        ]
        for event in due:
            if event.condition(self.state):
                for impact in event.impacts.split():
                    self.signals.store(impact)
                followups = event.apply(self.state)
                self.events.remove(event)
                for e in followups:
                    self.schedule(
                        e, f"follow-up from {event.type}"
                    )
        self._fulfill_rules()
        self.signals.notify()

    def _fulfill_rules(self):
        for rule in self.rules:
            for signal in self.signals._stored_signals:
                if signal in rule.listens_to:
                    for next_event in rule.fulfill(
                        self.state
                    ):
                        self.schedule(next_event, rule.name)
