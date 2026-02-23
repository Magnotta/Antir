from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    Float,
    Boolean,
    String,
    Text,
    JSON,
    ForeignKey,
    UniqueConstraint,
)


Base = declarative_base()


class Visit(Base):
    __tablename__ = "itinerary"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    toponym: Mapped[str] = mapped_column(
        String, nullable=False
    )
    arrival: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    departure: Mapped[int | None] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(Text)


class Path(Base):
    __tablename__ = "paths"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    origin_id: Mapped[int] = mapped_column(
        ForeignKey("localities.id"),
        nullable=False,
    )
    destination_id: Mapped[int] = mapped_column(
        ForeignKey("localities.id"),
        nullable=False,
    )
    distance_km: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String)
    data: Mapped[dict | None] = mapped_column(JSON)
    origin: Mapped["Locality"] = relationship(
        back_populates="outgoing_paths",
        foreign_keys=[origin_id],
    )
    destination: Mapped["Locality"] = relationship(
        back_populates="incoming_paths",
        foreign_keys=[destination_id],
    )
    point_conditions: Mapped[list["PointCondition"]] = (
        relationship(
            back_populates="path",
            cascade="all, delete-orphan",
            order_by="PointCondition.position",
        )
    )
    segment_conditions: Mapped[list["SegmentCondition"]] = (
        relationship(
            back_populates="path",
            cascade="all, delete-orphan",
            order_by="SegmentCondition.start",
        )
    )

    def __repr__(self):
        return f"<Path {self.origin_id} -> {self.destination_id}>"


class Locality(Base):
    __tablename__ = "localities"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String)
    data: Mapped[dict | None] = mapped_column(JSON)
    outgoing_paths: Mapped[list[Path]] = relationship(
        back_populates="origin",
        foreign_keys=[Path.origin_id],
        cascade="all, delete-orphan",
    )
    incoming_paths: Mapped[list[Path]] = relationship(
        back_populates="destination",
        foreign_keys=[Path.destination_id],
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"{self.name}"


class PointCondition(Base):
    __tablename__ = "point_conditions"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    path_id: Mapped[int] = mapped_column(
        ForeignKey("paths.id", ondelete="CASCADE"),
        nullable=False,
    )
    position: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    kind: Mapped[str] = mapped_column(
        String, nullable=False
    )
    data: Mapped[dict | None] = mapped_column(JSON)
    description: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    path: Mapped[Path] = relationship(
        back_populates="point_conditions"
    )


class SegmentCondition(Base):
    __tablename__ = "segment_conditions"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    path_id: Mapped[int] = mapped_column(
        ForeignKey("paths.id", ondelete="CASCADE"),
        nullable=False,
    )
    start: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    end: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    kind: Mapped[str] = mapped_column(
        String, nullable=False
    )
    data: Mapped[dict | None] = mapped_column(JSON)
    description: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    path: Mapped[Path] = relationship(
        back_populates="segment_conditions"
    )


class ParamSpec(Base):
    __tablename__ = "mold_param_specs"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    mold_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("molds.id"), nullable=False
    )
    param: Mapped[str] = mapped_column(
        String, nullable=False
    )
    base: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    variance: Mapped[int] = mapped_column(
        Integer, default=0
    )
    mold: Mapped["Mold"] = relationship(
        back_populates="param_specs"
    )
    __table_args__ = (UniqueConstraint("mold_id", "param"),)


class Mold(Base):
    __tablename__ = "molds"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(String, unique=True)
    tags: Mapped[str] = mapped_column(
        String, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String)
    occupied_slots: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    param_specs: Mapped[list[ParamSpec]] = relationship(
        back_populates="mold", cascade="all, delete-orphan"
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


class ItemParam(Base):
    __tablename__ = "item_params"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("items.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    value: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    parent_item: Mapped["Item"] = relationship(
        back_populates="param_list"
    )


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    original_mold_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("molds.id"),
        nullable=False,
    )
    owner_id: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    destroyed: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    param_list: Mapped[list[ItemParam]] = relationship(
        cascade="all, delete-orphan",
        back_populates="parent_item",
    )
    container_item_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("items.id"), nullable=True
    )
    container_item: Mapped["Item"] = relationship(
        back_populates="contained_items"
    )
    contained_items: Mapped[list["Item"]] = relationship(
        back_populates="container_item", remote_side=[id]
    )

    def __repr__(self):
        return (
            f"<Item id={self.id} mold={self.original_mold_id} "
            f"owner={self.owner_id} "
            f"container={self.container_item}>"
        )


class Character(Base):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )


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


class PlayerRecord(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String, nullable=False
    )


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


class EventRecord(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    type: Mapped[str] = mapped_column(
        String, nullable=False
    )
    payload: Mapped[dict | None] = mapped_column(
        JSON, nullable=False
    )
    due_tick: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    executed: Mapped[bool] = mapped_column(
        Boolean, default=False
    )
    origin: Mapped[str] = mapped_column(
        String, nullable=False
    )

    def __repr__(self):
        return f"executed at {self.due_tick} of type {self.type} with payload {self.payload}"
