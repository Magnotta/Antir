from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    String,
    JSON,
    Boolean,
    ForeignKey,
)
from db.models.base import Base


class Complication(Base):
    __tablename__ = "complications"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    key: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(
        String, nullable=False
    )
    blocking_flag: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"), nullable=False
    )
    participant_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"), nullable=False
    )
    problem_firing_id: Mapped[int | None] = mapped_column(
        ForeignKey("problems.id")
    )
    end_time: Mapped[int | None] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(String)


class ProblemFiring(Base):
    __tablename__ = "problems"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"), nullable=False
    )
    participant_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"), nullable=False
    )
    problem_kind: Mapped[str] = mapped_column(
        String, nullable=False
    )
    problem_key: Mapped[str] = mapped_column(
        String, nullable=False
    )
    time_tick: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    context_snapshot: Mapped[dict] = mapped_column(
        JSON, nullable=False
    )
    status: Mapped[str] = mapped_column(
        String, nullable=False
    )
    notes: Mapped[str | None] = mapped_column(String)
