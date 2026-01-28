from db.database import Session
from db.models import EventRecord
from engine.game_state import GameState
from systems.time_service import Time
from engine.events import Event, EVENTS

import heapq
from itertools import count

class ScheduledEvent:
    def __init__(self, record, event):
        self.record = record
        self.event = event

    def __lt__(self, other):
        return self.record.due_tick < other.record.due_tick

class Engine:
    def __init__(self):
        self.state = GameState()
        self.session = Session()
        self.events = []
        self._seq = count()

    def schedule(self, event: Event):
        rec = EventRecord(
            type=event.type,
            payload=event.payload,
            due_tick=event.due_tick,
            executed=False
        )
        self.session.add(rec)
        self.session.commit()

        heapq.heappush(
            self.queue,
            (event.due_tick, next(self._seq), rec, event)
        )

    def step(self):
        self.state.time.tick += 1
        self._dispatch_due_events()

    def _dispatch_due_events(self):
        while self.events and self.events[0][0] <= self.state.tick:
            _, _, rec, event = heapq.heappop(self.events)

            if rec.executed:
                print("Skip executed event")
                continue  # safety

            event.apply(self.state)
            rec.executed = True
            self.session.commit()

        for next_event in event.follow_up(self.state):
            self.schedule(next_event)

    def load_game(self, start_id) -> GameState:
        records = (
            self.session.query(EventRecord)
            .filter(EventRecord.executed.is_(False))
            .order_by(EventRecord.due_tick, EventRecord.id)
            .all()
        )

        for rec in records:
            event_cls = EVENTS[rec.type]
            event = event_cls(rec.payload, rec.due_tick)
            heapq.heappush(
                self.queue,
                (rec.due_tick, next(self._seq), rec, event)
            )