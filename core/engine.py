from db.database import Session
from db.models import EventRecord
from core.game_state import GameState
from systems.time_service import Time
from systems.command_service import CommandService
from core.events import Event, EVENTS
from core.rules import Rule



class Engine:
    def __init__(self):
        self.state = GameState()
        self.session = Session()
        self.cmd = CommandService(self)
        self.events:list[Event] = []
        self.rules:list[Rule] = []



    def schedule(self, event: Event, org: str):
        rec = EventRecord(
            type=event.type,
            payload=event.payload,
            due_tick=event.due_tick,
            origin = org
        )
        event._set_id(rec.id)
        self.session.add(rec)
        self.session.commit()


        self.events.append(event)
        self.events.sort(key=lambda e: e.due_tick)



    def step(self):
        self.state.time += 1
        self._dispatch_due_events()
        player_tab.refresh()



    def _dispatch_due_events(self):
        due:list[Event] = [
            e for e in self.events
            if e.due_tick <= self.state.time.tick
        ]

        for event in due:
            if event.condition(self.state):
                followups = event.apply(self.state)
                self.events.remove(event)

                for e in followups:
                    self.schedule(e, f"follow-up from {event.id}")

                self.session.commit()

                self._fulfill_rules(event)



    def _fulfill_rules(self, event):
        for rule in self.rules:
            if event.type in rule.listens_to:
                if rule.applies(event, self.state):
                    for next_event in rule.execute(event, self.state):
                        self.schedule(next_event, rule.name)



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