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


class StatThreshold(Base):
    __tablename__ = "stat_thresholds"
    id: Mapped[int] = mapped_column(primary_key=True)
    stat_name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    caution_high: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    critical_high: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    lose_control_high: Mapped[int | None] = mapped_column(
        Integer, nullable=False
    )


class HistoricalStat(Base):
    __tablename__ = "historical_stats"
    __table_args__ = (
        UniqueConstraint("player_id", "stat_name"),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.id"), nullable=False
    )
    stat_name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    all_time_max: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    last_updated: Mapped[int] = mapped_column(Integer)
