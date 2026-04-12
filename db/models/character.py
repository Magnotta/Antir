from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
)
from .base import Base


class Character(Base):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
