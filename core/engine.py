from collections import defaultdict
from sqlalchemy.orm import Session
from core.game_state import GameState
from core.rules import Rule, RULES
from core.events import Event
from db.repository.event import EventRepository
from systems.command_service import CommandService
from systems.signal_service import (
    SignalBus,
    Signal,
    SignalType,
)
from systems.summary_service import Summarizer


class Engine:
    def __init__(self, session: Session):
        self.session = session
        self.event_repo = EventRepository(session)
        self.state = GameState(session)
        self.cmd = CommandService(self)
        self.signals = SignalBus()
        self.summarizer = Summarizer(self.state)
        self.scheduled_events: list[Event] = []
        self.current_events: list[Event] = []
        self.signal_rule_map = defaultdict(list[Rule])
        for rule in RULES:
            for signal in rule.listens_to:
                self.signal_rule_map[signal].append(rule)

    def schedule(self, event: Event, org: str):
        self.event_repo.add_record(event, org)
        self.scheduled_events.append(event)

    def step(self):
        self._advance_time()
        self._dispatch_events()
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def _advance_time(self):
        self.signals.store([Signal(SignalType.minute, {})])
        if self.state.time.hour_change:
            self.signals.store(
                [Signal(SignalType.hour, {})]
            )
        if self.state.time.day_change:
            self.signals.store([Signal(SignalType.day, {})])
        self.state.time += 1
        self.state.update_time()

    def _dispatch_events(self):
        due = [
            e
            for e in self.scheduled_events
            if e.due_time <= self.state.time
        ]
        for event in due:
            if event.condition(self.state):
                apply_flag, concomitants = event.begin(
                    self.state
                )
                self.scheduled_events.remove(event)
                if apply_flag:
                    self.event_repo.add_record(
                        event, f"{event.type} begin"
                    )
                    self.current_events.append(event)
                    for e in concomitants:
                        self.current_events.append(e)
                    if event.tag:
                        self.scheduled_events = [
                            e
                            for e in self.scheduled_events
                            if e.tag != event.tag
                        ]
                else:
                    for e in concomitants:
                        self.schedule(
                            e,
                            f"rescheduled from {event.type}",
                        )

        running = [
            e
            for e in self.current_events
            if e.due_time <= self.state.time
        ]
        for event in running:
            follow_ups = event.apply(self.state)
            self.event_repo.add_record(
                event, f"{event.type} apply"
            )
            self.signals.store(event.get_signals())
            for e in follow_ups:
                self.schedule(
                    e, f"follow-up from {event.type}"
                )
            self.current_events.remove(event)
        self._fulfill_rules()
        self.signals.notify()

    def _fulfill_rules(self):
        for signal in self.signals._stored_signals:
            for rule in self.signal_rule_map.get(
                signal.type, []
            ):
                for next_event in rule.fulfill(
                    self.state, signal
                ):
                    self.schedule(next_event, rule.name)
