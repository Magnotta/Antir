from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from .base import Base


class ItemSlotOccupancy(Base):
    __tablename__ = "item_slot_occupancy"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("items.id"), nullable=False
    )
    equipment_slot_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("equipment_slots.id"),
        nullable=False,
    )
    __table_args__ = (
        UniqueConstraint(
            "equipment_slot_id",
            name="uix_slot_occupied_once",
        ),
    )
