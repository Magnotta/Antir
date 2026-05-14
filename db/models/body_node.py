from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Boolean,
    Text,
)
from .base import Base
from .equipment_slot import EquipmentSlot


class BodyNode(Base):
    __tablename__ = "body_nodes"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    broken_bone: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    torn_ligament: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    dislocated_joint: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    severed: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    venomous_bite: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    insect_bite: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    poison_sting: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    swollen_joint: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    sliced: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    pierced: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    bludgeoned: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    notes: Mapped[str] = mapped_column(Text, nullable=False)
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
