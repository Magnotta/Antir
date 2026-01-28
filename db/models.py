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

tags = [{"tagname": "we", "text": "armamento", "params":["durability", "quality", "wet", "mass", "com"]},
        {"tagname": "cu", "text": "cortante", "params":["sharpness"]},
        {"tagname": "bl", "text": "contundente", "params":["hardness"]},
        {"tagname": "pi", "text": "perfurante", "params":["pointiness"]},
        {"tagname": "ar", "text": "armadura", "params":["durability", "quality", "wet"]},
        {"tagname": "cl", "text": "vestimenta", "params":["elegance", "cleanliness", "wet"]},
        {"tagname": "wr", "text": "escrevível", "params":["fill", "wet"]},
        {"tagname": "rd", "text": "legível", "params":["clarity"]},
        {"tagname": "fl", "text": "inflamável", "params":["wet"]},
        {"tagname": "to", "text": "ferramenta", "params":["durability", "quality", "wet"]},
        {"tagname": "mt", "text": "material", "params":["quality", "purity"]},
        {"tagname": "pa", "text": "peça", "params":["durability", "quality"]},
        {"tagname": "un", "text": "unitário", "params":["count"]},
        {"tagname": "qt", "text": "quantificável", "params":["quantity", "units"]},
        {"tagname": "ed", "text": "comestível", "params":["aroma", "flavor", "rot"]},
        {"tagname": "lu", "text": "luminoso", "params":["power", "color"]},
        {"tagname": "co", "text": "conteiner", "params":["tightness"]},
        {"tagname": "en", "text": "energético", "params":["fill", "power"]},
        {"tagname": "dr", "text": "bebível", "params":["aroma", "flavor"]},
        {"tagname": "re", "text": "regenerante", "params":["intensity", "purity"]},
        {"tagname": "tx", "text": "tóxico", "params":["intensity"]},
        {"tagname": "wd", "text": "molha estraga", "params":["damage"]},
        {"tagname": "sy", "text": "psicoativo", "params":["intensity", "purity"]},
        {"tagname": "so", "text": "sonoro", "params":["power"]},
        {"tagname": "li", "text": "vivo", "params":["health"]}]

# tag_param_ranges = [{"durability":(0,1000)},
#                     {"quality":(0,4)},
#                     {"wet":(0,1000)},
#                     {"mass":(0,5)},
#                     {"com":(0,1000)},
#                     {"sharpness":(0,1000)},
#                     {"hardness":(0,1000)},
#                     {"pointiness":(,)},
#                     {"elegance":(,)},
#                     {"cleanliness":(,)},
#                     {"fill":(,)},
#                     {"clarity":(,)},
#                     {"purity":(,)},
#                     {"count":(,)},
#                     {"quantity":(,)},
#                     {"units":(,)},
#                     {"aroma":(,)},
#                     {"flavor":(,)},
#                     {"rot":(,)},
#                     {"power":(,)},
#                     {"color":(,)},
#                     {"capacity":(,)},
#                     {"intensity":(,)},
#                     {"damage":(,)},
#                     {"power":(,)}]

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
        return (self.id, self.name, self.type, self.tags)

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    original_mold = Column(Integer, ForeignKey('item_molds.id'))
    params = relationship('Item_Param')

class Item_Param(Base):
    __tablename__ = 'item_params'

    id = Column(Integer, primary_key=True)
    item = Column(Integer, ForeignKey('items.id'))
    param = Column(String, nullable=False)
    value = Column(Float, nullable=False)

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)

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