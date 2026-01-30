from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    ForeignKey,
    Float,
    JSON
)

Base = declarative_base()

itemmold_tags = [
    {"tagname": "we", "text": "armamento", "params":["durability","quality", "wet", "mass", "com"]},
    {"tagname": "cu", "text": "cortante", "params":["sharpness"]},
    {"tagname": "bl", "text": "contundente", "params":["roughness"]},
    {"tagname": "pi", "text": "perfurante", "params":["pointiness"]},
    {"tagname": "ar", "text": "armadura", "params":["durability", "hardness", "wet"]},
    {"tagname": "cl", "text": "vestimenta", "params":["elegance", "cleanliness", "wet"]},
    {"tagname": "wr", "text": "escrevível", "params":["fill", "wet"]},
    {"tagname": "rd", "text": "legível", "params":["clarity"]},
    {"tagname": "fl", "text": "inflamável", "params":["wet"]},
    {"tagname": "to", "text": "ferramenta", "params":["durability", "quality", "wet"]},
    {"tagname": "mt", "text": "material", "params":["quality", "purity"]},
    {"tagname": "pa", "text": "peça", "params":["durability", "quality"]},
    {"tagname": "cp", "text": "composição", "params":["durability", "integration"]},
    {"tagname": "un", "text": "unitário", "params":["count"]},
    {"tagname": "qt", "text": "quantificável", "params":["quantity"]},
    {"tagname": "ed", "text": "comestível", "params":["aroma", "flavor", "saturation", "nutrition", "rot"]},
    {"tagname": "lu", "text": "luminoso", "params":["power"]},
    {"tagname": "co", "text": "conteiner", "params":["leakage"]},
    {"tagname": "en", "text": "energético", "params":["fill", "power"]},
    {"tagname": "dr", "text": "bebível", "params":["aroma", "flavor", "saturation"]},
    {"tagname": "re", "text": "regenerante", "params":["power", "purity"]},
    {"tagname": "tx", "text": "tóxico", "params":["power"]},
    {"tagname": "wd", "text": "molha estraga", "params":["damage"]},
    {"tagname": "sy", "text": "psicoativo", "params":["power", "purity"]},
    {"tagname": "so", "text": "sonoro", "params":["power"]},
    {"tagname": "li", "text": "vivo", "params":["health"]}
]

item_params = [
    {"paramname":"durability","paramrange":1000},
    {"paramname":"quality","paramrange":4},
    {"paramname":"integration","paramrange":1000},
    {"paramname":"wet","paramrange":1000},
    {"paramname":"mass","paramrange":20},
    {"paramname":"com","paramrange":1000},
    {"paramname":"sharpness","paramrange":1000},
    {"paramname":"roughness","paramrange":1000},
    {"paramname":"pointiness","paramrange":1000},
    {"paramname":"hardness","paramrange":1000},
    {"paramname":"elegance","paramrange":5},
    {"paramname":"cleanliness","paramrange":1000},
    {"paramname":"fill","paramrange":1000},
    {"paramname":"clarity","paramrange":1000},
    {"paramname":"purity","paramrange":1000},
    {"paramname":"count","paramrange":1000000},
    {"paramname":"quantity","paramrange":10000},
    {"paramname":"aroma","paramrange":1000},
    {"paramname":"flavor","paramrange":1000},
    {"paramname":"rot","paramrange":1000},
    {"paramname":"power","paramrange":1000},
    {"paramname":"damage","paramrange":1000},
    {"paramname":"saturation","paramrange":1000},
    {"paramname":"nutrition","paramrange":1000},
    {"paramname":"leakage","paramrange":1000}
]

class Item_Mold(Base):
    __tablename__ = 'item_molds'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    type = Column(String, nullable=False)
    tags = Column(String, nullable=False)
    description = Column(String)

    def __repr__(self):
        return f'{str(self.id)}::{self.name}::{self.type}::{self.tags}::{self.description}'
    
    def as_tuple(self):
        return tuple(self.id, self.name, self.type, self.tags)

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    original_mold = Column(
        Integer,
        ForeignKey('item_molds.id'),
        nullable=False
    )
    owner = Column(Integer, nullable=False)
    param_list = relationship(
        "Item_Param",
        cascade="all, delete-orphan"
    )
    container_item_id = Column(
        Integer,
        ForeignKey('items.id'),
        nullable=True
    )
    container_item = relationship(
        "Item",
        back_populates="contained_items"
    )
    contained_items = relationship(
        "Item",
        back_populates="container_item",
        remote_side=[id]
    )

    def __repr__(self):
        return (
            f"<Item id={self.id} mold={self.original_mold} "
            f"owner={self.owner} container={self.container_item}>"
        )

class Item_Param(Base):
    __tablename__ = 'item_params'

    id = Column(Integer, primary_key=True)
    item = Column(Integer, ForeignKey('items.id'), nullable=False)
    param = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    parent_item = relationship(
        "Item",
        back_populates="param_list"
    )

class BodyNode(Base):
    __tablename__ = "body_nodes"

    id = Column(Integer, primary_key=True)
    owner = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("body_nodes.id"), nullable=True)
    parent = relationship(
        "BodyNode",
        remote_side=[id],
        back_populates="children"
    )
    children = relationship(
        "BodyNode",
        back_populates="parent"
    )
    slots = relationship(
        "EquipmentSlot",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<BodyNode {self.name} {self.health}/{self.max_health}>"
    
class EquipmentSlot(Base):
    __tablename__ = "equipment_slots"

    id = Column(Integer, primary_key=True)
    body_node_id = Column(
        Integer,
        ForeignKey("body_nodes.id"),
        nullable=False
    )
    slot_type = Column(String, nullable=False)
    slot_index = Column(Integer, default=0)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=True)

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

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