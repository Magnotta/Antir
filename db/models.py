from dataclasses import dataclass
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    ForeignKey,
    Float,
    JSON,
    UniqueConstraint,
)

Base = declarative_base()


class ItemMold(Base):
    __tablename__ = 'item_molds'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    tags = Column(String, nullable=False)
    description = Column(String)


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    original_mold = Column(
        Integer,
        ForeignKey('item_molds.id'),
        nullable=False,
    )
    owner = Column(Integer, nullable=False)
    param_list = relationship(
        "ItemParam", cascade="all, delete-orphan"
    )
    container_item_id = Column(
        Integer, ForeignKey('items.id'), nullable=True
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
            f"<Item id={self.id} mold={self.original_mold} "
            f"owner={self.owner}"
            f"container={self.container_item}>"
        )


class ItemParam(Base):
    __tablename__ = 'item_params'
    id = Column(Integer, primary_key=True)
    item = Column(
        Integer, ForeignKey('items.id'), nullable=False
    )
    param = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    parent_item = relationship(
        "Item", back_populates="param_list"
    )


class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)


class BodyNode(Base):
    __tablename__ = "body_nodes"
    id = Column(Integer, primary_key=True)
    health = Column(Integer, nullable=False)
    owner = Column(Integer, nullable=False)
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
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class PlayerStat(Base):
    __tablename__ = 'player_stats'
    id = Column(Integer, primary_key=True)
    player_id = Column(
        Integer, ForeignKey("players.id"), nullable=False
    )
    name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    __table_args__ = (
        UniqueConstraint("player_id", "name"),
    )


@dataclass(frozen=True)
class Sickness:
    id: int = 0
    name: str = ""
    description: str = ""
    contagious: bool = False


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    toponym = Column(String, nullable=False)
    arrival = Column(Integer, nullable=False)
    departure = Column(Integer)
    description = Column(String)


class EventRecord(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    due_tick = Column(Integer, nullable=False)
    executed = Column(Boolean, default=False)
    origin = Column(String, nullable=False)
