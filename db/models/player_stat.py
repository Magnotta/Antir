from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
)
from .base import Base


class PlayerStat(Base):
    __tablename__ = "player_stats"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    value: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    __table_args__ = (
        UniqueConstraint("player_id", "name"),
    )
