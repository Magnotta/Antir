from db.repository import (
    EventRepository,
    ItemRepository,
    PlayerRepository,
    LocationRepository,
)
from core.game_state import GameState
from core.rules import RULES
from player.domain import Player
from systems.command_service import CommandService
from systems.signal_service import SignalBus, Signal


class Engine:
    def __init__(
        self,
        event_repo: EventRepository,
        item_repo: ItemRepository,
        player_repo: PlayerRepository,
        loc_repo: LocationRepository,
        players: list[Player],
    ):
        self.state = GameState(
            event_repo, item_repo, player_repo, loc_repo, players
        )
        self.cmd = CommandService(self)
        self.signals = SignalBus()
        self.events = []
        self.rules = RULES

    def schedule(self, event, org: str):
        self.state.event_repo.add_record(event, org)
        self.events.append(event)
        self.events.sort(key=lambda e: e.due_time)

    def step(self):
        self._advance_time()
        self._dispatch_due_events()

    def _advance_time(self):
        self.state.time += 1
        self.signals.store([Signal.minute])
        if self.state.time.hour_change:
            self.signals.store([Signal.hour])
        if self.state.time.day_change:
            self.signals.store([Signal.day])

    def _dispatch_due_events(self):
        due = [
            e
            for e in self.events
            if e.due_time <= self.state.time
        ]
        for event in due:
            if event.condition(self.state):
                self.signals.store(event.signals)
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
