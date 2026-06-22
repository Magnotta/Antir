from db.repository.item import ItemRepository
from db.repository.event import EventRepository
from db.repository.location import LocationRepository
from db.repository.player import PlayerRepository
from db.repository.global_var import GlobalVarRepository
from core.game_state import GameState
from core.rules import Rule, RULES
from core.events import Event
from player.domain import Player
from systems.command_service import CommandService
from systems.signal_service import SignalBus, Signal
from systems.summary_service import Summarizer


class Engine:
    def __init__(
        self,
        event_repo: EventRepository,
        item_repo: ItemRepository,
        player_repo: PlayerRepository,
        loc_repo: LocationRepository,
        var_repo: GlobalVarRepository,
        players: list[Player],
    ):
        self.state = GameState(
            event_repo,
            item_repo,
            player_repo,
            loc_repo,
            var_repo,
            players,
        )
        self.cmd = CommandService(self)
        self.signals = SignalBus()
        self.summarizer = Summarizer(self.state)
        self.scheduled_events: list[Event] = []
        self.current_events: list[Event] = []
        self.rules: list[Rule] = RULES

    def schedule(self, event: Event, org: str):
        self.state.event_repo.add_record(event, org)
        self.scheduled_events.append(event)

    def _follow_up(self, event: Event, org: str):
        self.state.event_repo.add_record(event, org)
        self.current_events.append(event)

    def step(self):
        self._advance_time()
        self._dispatch_events()

    def _advance_time(self):
        self.state.time += 1
        self.signals.store([Signal.minute])
        if self.state.time.hour_change:
            self.signals.store([Signal.hour])
        if self.state.time.day_change:
            self.signals.store([Signal.day])

    def _dispatch_events(self):
        due = [
            e
            for e in self.scheduled_events
            if e.due_time <= self.state.time
        ]
        for event in due:
            if event.condition(self.state):
                self.signals.store(event.emits_signals)
                followups = event.begin(self.state)
                self.scheduled_events.remove(event)
                for e in followups:
                    self._follow_up(
                        e, f"follow-up from {event.type}"
                    )
        running = [
            e
            for e in self.current_events
            if e.due_time <= self.state.time
        ]
        for event in running:
            self.signals.store(event.emits_signals)
            event.apply(self.state)
            self.current_events.remove(event)
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
