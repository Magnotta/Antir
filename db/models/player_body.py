from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from db.models.base import Base


class BodyNode(Base):
    __tablename__ = "body_nodes"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    broken_bone: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    torn_ligament: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    muscle_strain: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    dislocated_joint: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    severed: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    venomous_bite: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    insect_bite: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    poison_sting: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    swollen_joint: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    sunburn: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    dermatitis: Mapped[int] = mapped_column(
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
    slots: Mapped[list["EquipmentSlot"]] = relationship(
        cascade="all, delete-orphan"
    )


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
