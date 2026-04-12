from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
)
from .base import Base


class EquipmentSlot(Base):
    __tablename__ = "equipment_slots"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    body_node_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("body_nodes.id"), nullable=False
    )
    slot_type: Mapped[str] = mapped_column(
        String, nullable=False
    )
    slot_index: Mapped[int] = mapped_column(
        Integer, default=0
    )
    item_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("items.id"), nullable=True
    )
