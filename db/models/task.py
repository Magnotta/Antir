from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import Integer, String, JSON, ForeignKey
from sqlalchemy.ext.mutable import MutableList, MutableDict
from db.models.base import Base


class TaskSpec(Base):
    __tablename__ = "task_specs"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    task_preset: Mapped[str] = mapped_column(
        String, nullable=False
    )
    total_workload: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    cooperation_profile: Mapped[str | None] = mapped_column(
        String
    )
    output: Mapped[dict | None] = mapped_column(JSON)
    workstation_type: Mapped[str | None] = mapped_column(
        String
    )
    duration_override_ticks: Mapped[int | None] = (
        mapped_column(Integer)
    )
    problems: Mapped[dict] = mapped_column(
        JSON, nullable=False
    )
    notes: Mapped[str | None] = mapped_column(String)


class TaskInstance(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    participant_ids: Mapped[list[int]] = mapped_column(
        MutableList.as_mutable(JSON), default=list
    )
    location: Mapped[int] = mapped_column(
        ForeignKey("sites.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String, nullable=False
    )
    task_spec_id: Mapped[int] = mapped_column(
        ForeignKey("task_specs.id"), nullable=False
    )
    workstation_id: Mapped[int | None] = mapped_column(
        Integer
    )
    task_item_dict: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSON), default=dict
    )
    task_output: Mapped[dict | None] = mapped_column(JSON)
    workload_total: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    workload_done: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    effective_problems: Mapped[dict] = mapped_column(
        JSON, nullable=False
    )
    notes: Mapped[str | None] = mapped_column(String)


class TaskParticipation(Base):
    __tablename__ = "task_participations"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    participant_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"), nullable=False
    )
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"), nullable=False
    )
    started_at: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    workload_buffer: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
