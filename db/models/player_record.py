from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    String,
)
from .base import Base


class PlayerRecord(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String, nullable=False
    )
