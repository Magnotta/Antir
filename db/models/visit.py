from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    String,
    Text,
)
from .base import Base


class Visit(Base):
    __tablename__ = "itinerary"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    toponym: Mapped[str] = mapped_column(
        String, nullable=False
    )
    arrival: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    departure: Mapped[int | None] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(Text)
