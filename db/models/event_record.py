from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    Boolean,
    String,
    JSON,
)
from .base import Base


class EventRecord(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    type: Mapped[str] = mapped_column(
        String, nullable=False
    )
    payload: Mapped[dict | None] = mapped_column(
        JSON, nullable=False
    )
    due_tick: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    executed: Mapped[bool] = mapped_column(
        Boolean, default=False
    )
    origin: Mapped[str] = mapped_column(
        String, nullable=False
    )

    def __repr__(self):
        return f"executed at {self.due_tick} of type {self.type} with payload {self.payload}"
