from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import Integer, String, JSON
from db.models.base import Base


class TaskGroupRecord(Base):
    __tablename__ = "task_groups"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    task_spec: Mapped[str] = mapped_column(
        String, nullable=False
    )
    started_at: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    expected_duration_ticks: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    spec: Mapped[dict] = mapped_column(
        JSON, nullable=False
    )  # serialized TaskSpec
    participant_ids: Mapped[list] = mapped_column(
        JSON, nullable=False
    )
