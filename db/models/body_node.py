from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
)
from .base import Base
from .equipment_slot import EquipmentSlot


class BodyNode(Base):
    __tablename__ = "body_nodes"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    health: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    owner_id: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("body_nodes.id"), nullable=True
    )
    parent: Mapped["BodyNode | None"] = relationship(
        remote_side=[id], back_populates="children"
    )
    children: Mapped[list["BodyNode"]] = relationship(
        back_populates="parent"
    )
    slots: Mapped[list[EquipmentSlot]] = relationship(
        cascade="all, delete-orphan"
    )
