from sqlalchemy.orm import Session
from db.models.event_record import EventRecord


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_record(self, event, org: str):
        rec = EventRecord(
            type=event.type,
            payload=event.payload,
            due_tick=event.due_time.tick,
            origin=org,
        )
        self.session.add(rec)
        self.session.commit()
