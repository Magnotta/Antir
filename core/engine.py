from db.models import EventRecord
from core.game_state import GameState
from core.events import Event, EVENTS
from core.rules import Rule, RULES
from player.domain import Player
from systems.command_service import CommandService
from systems.signal_service import SignalBus


class Engine:
    def __init__(self, session, players: list[Player]):
        self.state = GameState(players)
        self.session = session
        self.cmd = CommandService(self)
        self.events: list[Event] = []
        self.rules: list[Rule] = RULES
        self.signals = SignalBus()

    def schedule(self, event: Event, org: str):
        rec = EventRecord(
            type=event.type,
            payload=event.payload,
            due_tick=event.due_time.tick,
            origin=org,
        )
        event._set_id(rec.id)
        self.session.add(rec)
        self.session.commit()
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
        due: list[Event] = [
            e for e in self.events if e.due_time <= self.state.time
        ]
        for event in due:
            if event.condition(self.state):
                for impact in event.impacts.split():
                    self.signals.store(impact)
                followups = event.apply(self.state)
                self.events.remove(event)
                for e in followups:
                    self.schedule(e, f"follow-up from {event.id}")
                self.session.commit()
        self._fulfill_rules()
        self.signals.notify()

    def _fulfill_rules(self):
        for rule in self.rules:
            for signal in self.signals._stored_signals:
                if signal in rule.listens_to:
                    for next_event in rule.fulfill(self.state):
                        self.schedule(next_event, rule.name)

    def load_game(self, start_id: int) -> GameState:
        records = (
            self.session.query(EventRecord)
            .filter(EventRecord.executed.is_(False))
            .order_by(EventRecord.due_tick, EventRecord.id)
            .all()
        )
        for rec in records:
            event_cls = EVENTS[rec.type]
            event = event_cls(rec.payload, rec.due_tick)
            self.events.append(event)
