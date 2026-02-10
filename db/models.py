from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    ForeignKey,
    JSON,
    UniqueConstraint,
)

Base = declarative_base()


class ParamSpec(Base):
    __tablename__ = "mold_param_specs"
    id = Column(Integer, primary_key=True)
    mold_id = Column(
        Integer, ForeignKey("molds.id"), nullable=False
    )
    param = Column(String, nullable=False)
    base = Column(Integer, nullable=False)
    variance = Column(Integer, default=0)
    mold = relationship(
        "Mold", back_populates="param_specs"
    )
    __table_args__ = (UniqueConstraint("mold_id", "param"),)


class Mold(Base):
    __tablename__ = "molds"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    tags = Column(String, nullable=False)
    description = Column(String)
    occupied_slots = Column(JSON, nullable=True)
    param_specs = relationship(
        "ParamSpec", cascade="all, delete-orphan"
    )


class ItemSlotOccupancy(Base):
    __tablename__ = "item_slot_occupancy"
    id = Column(Integer, primary_key=True)
    item_id = Column(
        Integer, ForeignKey("items.id"), nullable=False
    )
    equipment_slot_id = Column(
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


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    original_mold_id = Column(
        Integer,
        ForeignKey("molds.id"),
        nullable=False,
    )
    owner_id = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    param_list = relationship(
        "ItemParam",
        cascade="all, delete-orphan",
        back_populates="parent_item",
    )
    container_item_id = Column(
        Integer, ForeignKey("items.id"), nullable=True
    )
    container_item = relationship(
        "Item", back_populates="contained_items"
    )
    contained_items = relationship(
        "Item",
        back_populates="container_item",
        remote_side=[id],
    )

    def __repr__(self):
        return (
            f"<Item id={self.id} mold={self.original_mold_id} "
            f"owner={self.owner_id}"
            f"container={self.container_item}>"
        )


class ItemParam(Base):
    __tablename__ = "item_params"
    id = Column(Integer, primary_key=True)
    item_id = Column(
        Integer, ForeignKey("items.id"), nullable=False
    )
    name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    parent_item = relationship(
        "Item", back_populates="param_list"
    )


class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)


class BodyNode(Base):
    __tablename__ = "body_nodes"
    id = Column(Integer, primary_key=True)
    health = Column(Integer, nullable=False)
    owner_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    parent_id = Column(
        Integer, ForeignKey("body_nodes.id"), nullable=True
    )
    parent = relationship(
        "BodyNode",
        remote_side=[id],
        back_populates="children",
    )
    children = relationship(
        "BodyNode", back_populates="parent"
    )
    slots = relationship(
        "EquipmentSlot", cascade="all, delete-orphan"
    )


class EquipmentSlot(Base):
    __tablename__ = "equipment_slots"
    id = Column(Integer, primary_key=True)
    body_node_id = Column(
        Integer,
        ForeignKey("body_nodes.id"),
        nullable=False,
    )
    slot_type = Column(String, nullable=False)
    slot_index = Column(Integer, default=0)
    item_id = Column(
        Integer, ForeignKey("items.id"), nullable=True
    )


class PlayerRecord(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class PlayerStat(Base):
    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True)
    player_id = Column(
        Integer, ForeignKey("players.id"), nullable=False
    )
    name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    __table_args__ = (
        UniqueConstraint("player_id", "name"),
    )


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    toponym = Column(String, nullable=False)
    arrival = Column(Integer, nullable=False)
    departure = Column(Integer)
    description = Column(String)


class EventRecord(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    due_tick = Column(Integer, nullable=False)
    executed = Column(Boolean, default=False)
    origin = Column(String, nullable=False)
